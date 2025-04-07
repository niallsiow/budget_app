from django.db import models
from django.utils.timezone import now
from django.urls import reverse


# Modify later to include currency type in Account model
#   can be used for display purposes in views
class Account(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=20, decimal_places=2)

    def get_absolute_url(self):
        return reverse("account_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.user} {self.name} {self.balance}"


# leaving Categories out for now, not sure how I want to implement the form for this yet

# class Category(models.Model):
#     name = models.CharField(max_length=100)
# 
#     def __str__(self):
#         return self.name


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    date = models.DateField(default=now)
    
    # category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.date}: {self.amount}"


# class RecurringTransaction(models.Model):
#     account = models.ForeignKey(Account, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=18, decimal_places=2)
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
#     date = models.DateField(default=now)

#     def __str__(self):
#         return f"{self.date}: {self.amount}"
