from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Account


class AccountListView(ListView):
    model = Account
    template_name = "home.html"


class AccountDetailView(DetailView):
    model = Account
    template_name = "account_detail.html"


class AccountCreateView(CreateView):
    model = Account
    template_name = "account_new.html"
    fields = ["name", "balance"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)