from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction

@receiver(post_save, sender=Transaction)
def update_account_balance(sender, instance , created ,**kwargs):
    if created:
        account = instance.account
        category  = instance.category

        if category.is_income:
            account.balance += instance.amount
        else:
            account.balance -= instance.amount
        
        account.save()