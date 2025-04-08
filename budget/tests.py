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
        cls.account = Account.objects.create(user=cls.user, name="Test Account")

    def test_account_model(self):
        self.assertEqual(self.account.name, "Test Account")

    def test_url_exists_at_correct_location_listview(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_account_listview(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.account.name)
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
        self.assertContains(response, self.account.name)
        self.assertTemplateUsed(response, "account_detail.html")

    def test_account_createview(self):
        self.client.login(username="testuser", password="secret")

        response = self.client.get(reverse("account_new"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account_new.html")

        response = self.client.post(
            reverse("account_new"),
            {
                "name": "New Account",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Account.objects.last().name, "New Account")
        self.assertRedirects(
            response,
            reverse(
                "account_detail",
                kwargs={"pk": Account.objects.get(name="New Account").id},
            ),
        )

    def test_account_editview(self):
        self.client.login(username="testuser", password="secret")
        new_account = Account.objects.create(user=self.user, name="New Account")

        response = self.client.get(
            reverse("account_edit", kwargs={"pk": new_account.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, new_account.name)
        self.assertTemplateUsed(response, "account_edit.html")

        response = self.client.post(
            reverse("account_edit", kwargs={"pk": new_account.pk}),
            {
                "name": "Edited Account",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Account.objects.last().name, "Edited Account")
        self.assertRedirects(
            response, reverse("account_detail", kwargs={"pk": new_account.id})
        )

    def test_account_deleteview(self):
        self.client.login(username="testuser", password="secret")
        new_account = Account.objects.create(user=self.user, name="New Account")
        self.assertTrue(Account.objects.filter(id=new_account.id).exists())

        response = self.client.get(
            reverse("account_delete", kwargs={"pk": new_account.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, new_account.name)
        self.assertTemplateUsed(response, "account_delete.html")

        response = self.client.post(
            reverse("account_delete", kwargs={"pk": new_account.pk})
        )
        self.assertFalse(Account.objects.filter(id=new_account.id).exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    def test_account_access(self):
        new_user = get_user_model().objects.create_user(
            username="newuser", email="newuser@email.com", password="secret"
        )

        self.client.login(username="newuser", password="secret")

        # Attempt to access detail view of class object, should fail
        response = self.client.get("/account/1/")
        self.assertEqual(response.status_code, 404)

    def test_signup(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("registration/signup.html")

        response = self.client.post(
            reverse("signup"),
            {
                "username": "signuptestuser",
                "password1": "testpass123",
                "password2": "testpass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

    def test_login(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("registration/login.html")

        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "secret"}
        )
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    def test_logout(self):
        self.client.login(username="testuser", password="secret")

        response = self.client.get(reverse("home"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, "Log Out")

        response = self.client.post(reverse("logout"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
