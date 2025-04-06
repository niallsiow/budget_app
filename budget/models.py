from django.db import models
from django.utils.timezone import now


# Just add models and fields one at a time, figure out the rendering etc.
# happy enough with the current commented out models setup though


# Modify later to include currency type in Account model
#   can be used for display purposes in views
class Account(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"{self.user} {self.name} {self.balance}"


# class Category(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name


# class Transaction(models.Model):
#     account = models.ForeignKey(Account, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=18, decimal_places=2)
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
#     date = models.DateField(default=now)

#     def __str__(self):
#         return f"{self.date}: {self.amount}"


# class RecurringTransaction(models.Model):
#     account = models.ForeignKey(Account, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=18, decimal_places=2)
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
#     date = models.DateField(default=now)

#     def __str__(self):
#         return f"{self.date}: {self.amount}"
