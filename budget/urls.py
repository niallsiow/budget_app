from django.urls import path
from .views import (
    AccountListView,
    AccountDetailView,
    AccountCreateView,
    AccountUpdateView,
    AccountDeleteView,
    TransactionCreateView,
    TransactionUpdateView,
    TransactionDeleteView,
)

urlpatterns = [
    path("", AccountListView.as_view(), name="home"),
    path("account/<int:pk>/", AccountDetailView.as_view(), name="account_detail"),
    path("account/new/", AccountCreateView.as_view(), name="account_new"),
    path("account/<int:pk>/edit/", AccountUpdateView.as_view(), name="account_edit"),
    path(
        "account/<int:pk>/delete/", AccountDeleteView.as_view(), name="account_delete"
    ),
    path("transaction/new/", TransactionCreateView.as_view(), name="transaction_new"),
    path("transaction/<int:pk>/edit/", TransactionUpdateView.as_view(), name="transaction_edit"),
    path("transaction/<int:pk>/delete/", TransactionDeleteView.as_view(), name="transaction_delete"),
]
