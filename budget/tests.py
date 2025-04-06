from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Account


class BudgetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com", password="secret"
        )
        cls.account = Account.objects.create(
            user=cls.user, name="Test Account", balance=2000
        )

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

    def test_url_exists_at_correct_location_detailview(self):
        response = self.client.get("/account/1/")
        self.assertEqual(response.status_code, 200)

    def test_account_detail_view(self):
        response = self.client.get(reverse("account_detail", kwargs={"pk": self.account.pk}))
        no_response = self.client.get("/account/10000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Test Account")
        self.assertTemplateUsed(response, "account_detail.html")

    def test_post_createview(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.post(
            reverse("account_new"),
            {
                "name": "New Account",
                "balance": 5000,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Account.objects.last().name, "New Account")
        self.assertEqual(Account.objects.last().balance, 5000)