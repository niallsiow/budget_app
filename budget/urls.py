from django.urls import path
from .views import AccountListView, AccountDetailView, AccountCreateView

urlpatterns = [
    path("", AccountListView.as_view(), name="home"),
    path("account/<int:pk>/", AccountDetailView.as_view(), name="account_detail"),
    path("account/new/", AccountCreateView.as_view(), name="account_new"),
]
