from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.urls import reverse, reverse_lazy

from .models import Account, Transaction


class AccountListView(ListView):
    model = Account
    template_name = "home.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Account.objects.filter(user=self.request.user)


class AccountDetailView(DetailView):
    model = Account
    template_name = "account_detail.html"

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class AccountCreateView(CreateView):
    model = Account
    template_name = "account_new.html"
    fields = ["name"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AccountUpdateView(UpdateView):
    model = Account
    template_name = "account_edit.html"
    fields = ["name"]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class AccountDeleteView(DeleteView):
    model = Account
    template_name = "account_delete.html"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class TransactionCreateView(CreateView):
    model = Transaction
    template_name = "transaction_new.html"
    fields = ["account", "amount", "date"]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["account"].queryset = Account.objects.filter(user=self.request.user)
        return form

    def get_success_url(self):
        return reverse("account_detail", kwargs={"pk": self.object.account.pk})


class TransactionUpdateView(UpdateView):
    model = Transaction
    template_name = "transaction_edit.html"
    fields = ["amount", "date"]

    def get_success_url(self):
        return reverse("account_detail", kwargs={"pk": self.object.account.pk})


class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = "transaction_delete.html"
    success_url = reverse_lazy("home")
