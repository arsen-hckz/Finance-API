from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from .models import Account, Category, Transaction


class FinanceAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('alice', password='Str0ng-pass-123')
        self.other = User.objects.create_user('bob', password='Str0ng-pass-123')
        self.account = Account.objects.create(user=self.user, name='Bank', balance=Decimal('100.00'))
        self.other_account = Account.objects.create(user=self.other, name='Bob bank', balance=Decimal('50.00'))
        self.salary = Category.objects.create(name='Salary', is_income=True)
        self.food = Category.objects.create(name='Food', is_income=False)
        self.client.force_authenticate(self.user)

    def post_transaction(self, **overrides):
        body = {'account': self.account.id, 'category': self.food.id, 'amount': '10.00', 'description': 'x'}
        body.update(overrides)
        return self.client.post('/api/transactions/', body, format='json')

    def balance(self, account):
        account.refresh_from_db()
        return account.balance

    # Auth

    def test_register_and_login_with_jwt(self):
        self.client.force_authenticate(None)
        res = self.client.post('/auth/users/', {'username': 'carol', 'password': 'An0ther-pass-456',
                                                're_password': 'An0ther-pass-456'}, format='json')
        self.assertEqual(res.status_code, 201)
        res = self.client.post('/auth/jwt/create/', {'username': 'carol', 'password': 'An0ther-pass-456'}, format='json')
        self.assertEqual(res.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")
        self.assertEqual(self.client.get('/api/accounts/').status_code, 200)

    def test_endpoints_need_login(self):
        self.client.force_authenticate(None)
        for path in ('/api/accounts/', '/api/transactions/', '/api/categories/'):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 401)

    # Balances

    def test_expense_subtracts_from_balance(self):
        self.assertEqual(self.post_transaction(amount='30.50').status_code, 201)
        self.assertEqual(self.balance(self.account), Decimal('69.50'))

    def test_income_adds_to_balance(self):
        self.assertEqual(self.post_transaction(category=self.salary.id, amount='1200.00').status_code, 201)
        self.assertEqual(self.balance(self.account), Decimal('1300.00'))

    def test_several_transactions_add_up(self):
        self.post_transaction(amount='10.00')
        self.post_transaction(amount='15.25')
        self.post_transaction(category=self.salary.id, amount='5.00')
        self.assertEqual(self.balance(self.account), Decimal('79.75'))

    def test_amount_must_be_positive(self):
        for amount in ('0', '-10.00', 'abc', 'NaN'):
            with self.subTest(amount=amount):
                self.assertEqual(self.post_transaction(amount=amount).status_code, 400)
        self.assertEqual(self.balance(self.account), Decimal('100.00'))
        self.assertFalse(Transaction.objects.exists())

    # Ownership

    def test_cannot_post_to_another_users_account(self):
        res = self.post_transaction(account=self.other_account.id, amount='50.00')
        self.assertEqual(res.status_code, 400)
        self.assertEqual(self.balance(self.other_account), Decimal('50.00'))

    def test_only_own_accounts_are_listed(self):
        res = self.client.get('/api/accounts/')
        self.assertEqual([a['id'] for a in res.data], [self.account.id])

    def test_only_own_transactions_are_listed(self):
        Transaction.objects.create(account=self.other_account, category=self.food, amount=Decimal('1'), description='bob')
        self.post_transaction()
        res = self.client.get('/api/transactions/')
        self.assertEqual([t['description'] for t in res.data], ['x'])

    def test_new_account_belongs_to_requester(self):
        res = self.client.post('/api/accounts/', {'name': 'Cash', 'user': self.other.id}, format='json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Account.objects.get(id=res.data['id']).user, self.user)

    # Categories and filtering

    def test_categories_are_listed(self):
        res = self.client.get('/api/categories/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual({c['name'] for c in res.data}, {'Salary', 'Food'})

    def test_filter_transactions_by_category(self):
        self.post_transaction(description='lunch')
        self.post_transaction(category=self.salary.id, description='pay')
        res = self.client.get(f'/api/transactions/?category={self.salary.id}')
        self.assertEqual(res.status_code, 200)
        self.assertEqual([t['description'] for t in res.data], ['pay'])

    def test_bad_category_filter_is_400(self):
        for value in ('abc', '-1', '1.5', '9' * 30):
            with self.subTest(value=value):
                self.assertEqual(self.client.get(f'/api/transactions/?category={value}').status_code, 400)
