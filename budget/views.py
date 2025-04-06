from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Account


class AccountListView(ListView):
    model = Account
    template_name = "home.html"


class AccountDetailView(DetailView):
    model = Account
    template_name = "account_detail.html"
