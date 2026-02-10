from rest_framework import serializers
from .models import Account,Category,Transaction

class AccountSerializer(serializers.ModelSerializer):
      class Meta:  
        model = Account
        fields = ['id','name','balance']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all_"

class TransactionSeriliazer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source = 'category.name')
    class Meta:
        model = Transaction
        fields = ['amount','account','description','date','category','category_name']
        