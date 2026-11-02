import re

from django.db import transaction
from django.shortcuts import render
from rest_framework import generics,permissions
from rest_framework.exceptions import ValidationError
from .serializers import TransactionSeriliazer,AccountSerializer,CategorySerializer
from .models import Account,Transaction,Category


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class AccountView(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user= self.request.user)
    
    def perform_create(self,serializer):
        serializer.save(user = self.request.user)

class TransactionView(generics.ListCreateAPIView):
    serializer_class = TransactionSeriliazer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Transaction.objects.filter(account__user = user)
        category = self.request.query_params.get('category')
        if category:
            if not re.fullmatch(r'\d{1,18}', category):
                raise ValidationError({'category': 'Must be a category id.'})
            return queryset.filter(category_id = int(category))
        return queryset
        
    def perform_create(self,serializer):
        # The transaction row and the balance update (signal) succeed or fail together.
        with transaction.atomic():
            serializer.save()


