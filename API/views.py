from django.shortcuts import render
from rest_framework import generics,permissions
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
            return queryset.filter(category_id = 'category')
        return queryset
        
    def perform_create(self,serializer):
        serializer.save()


