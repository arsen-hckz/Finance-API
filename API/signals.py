from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account, Transaction

@receiver(post_save, sender=Transaction)
def update_account_balance(sender, instance , created ,**kwargs):
    if created:
        change = instance.amount if instance.category.is_income else -instance.amount
        # Done in the database (balance = balance + change), so two transactions
        # saved at the same time can't both read the old balance and lose one.
        Account.objects.filter(pk=instance.account_id).update(balance=F('balance') + change)
