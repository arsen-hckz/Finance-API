from decimal import Decimal

from rest_framework import serializers
from .models import Account,Category,Transaction

class AccountSerializer(serializers.ModelSerializer):
      class Meta:
        model = Account
        fields = ['id','name','balance']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class TransactionSeriliazer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source = 'category.name')
    # Always positive: the category decides whether it's added or subtracted.
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal('0.01'))
    class Meta:
        model = Transaction
        fields = ['amount','account','description','date','category','category_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only the requesting user's accounts are valid choices, so another
        # user's account id gets the same "does not exist" error as a missing one.
        request = self.context.get('request')
        if request is not None:
            self.fields['account'].queryset = Account.objects.filter(user=request.user)
