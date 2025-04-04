from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Account

class BudgetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="testuser", email="test@email.com", password="secret")
        cls.account = Account.objects.create(user=cls.user, name="Test Account", balance=2000)        

    def test_account_model(self):
        self.assertEqual(self.account.name, "Test Account")
        self.assertEqual(self.account.balance, 2000)

    def test_url_exists_at_correct_location_listview(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_account_list_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Account")
        self.assertTemplateUsed(response, "home.html")