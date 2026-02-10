from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,db_index=True)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=12,decimal_places=2,default=0.00)

    def __str__(self):
        return f"{self.name} - {self.balance}€"
    
class Category(models.Model):
    name  = models.CharField(max_length=100,db_index=True)
    is_income = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.name} - {self.is_income}"
    
class Transaction(models.Model):
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,db_index=True)
    amount = models.DecimalField(max_digits=12,decimal_places=2)
    description = models.TextField(max_length=1000)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date']