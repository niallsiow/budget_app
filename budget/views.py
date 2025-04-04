from django.shortcuts import render
from django.views.generic import ListView

from .models import Account


class AccountListView(ListView):
    model = Account
    template_name = "home.html"
