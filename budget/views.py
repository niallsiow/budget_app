from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy

from .models import Account


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
    fields = ["name", "balance"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AccountUpdateView(UpdateView):
    model = Account
    template_name = "account_edit.html"
    fields = ["name", "balance"]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class AccountDeleteView(DeleteView):
    model = Account
    template_name = "account_delete.html"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)