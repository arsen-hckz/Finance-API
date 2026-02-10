from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Account, Category, Transaction

# Basic registration so they show up in the admin
admin.site.register(Account)
admin.site.register(Category)

# Pro-tip: Register Transaction with list_display to see details at a glance
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'category', 'amount')
    list_filter = ('category', 'account')