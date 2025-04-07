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

    def test_account_listview(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Account")
        self.assertTemplateUsed(response, "home.html")

    def test_url_exists_at_correct_location_detailview(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get("/account/1/")
        self.assertEqual(response.status_code, 200)

    def test_account_detailview(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(
            reverse("account_detail", kwargs={"pk": self.account.pk})
        )
        no_response = self.client.get("/account/10000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Test Account")
        self.assertTemplateUsed(response, "account_detail.html")

    def test_account_createview(self):
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

    def test_account_editview(self):
        self.client.login(username="testuser", password="secret")

        new_account = Account.objects.create(
            user=self.user, name="New Account", balance=5
        )

        response = self.client.post(
            reverse("account_edit", kwargs={"pk": new_account.pk}),
            {
                "name": "Edited Account",
                "balance": 20,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Account.objects.last().name, "Edited Account")
        self.assertEqual(Account.objects.last().balance, 20)

    def test_account_deleteview(self):
        self.client.login(username="testuser", password="secret")
        new_account = Account.objects.create(
            user=self.user, name="New Account", balance=5
        )
        self.assertTrue(Account.objects.filter(id=new_account.id).exists())

        response = self.client.post(
            reverse("account_delete", kwargs={"pk": new_account.pk})
        )
        self.assertFalse(Account.objects.filter(id=new_account.id).exists())
