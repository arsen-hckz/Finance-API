from django.urls import path , include
from .views import AccountView,TransactionView,CategoryView

urlpatterns = [
path('categories/', CategoryView.as_view()),
path('accounts/',AccountView.as_view()),
path('transactions/', TransactionView.as_view()),


]