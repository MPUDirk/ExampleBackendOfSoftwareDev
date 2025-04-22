import time

from django.db import models

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(to='auth.User', on_delete=models.CASCADE)
    address = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Good(models.Model):
    group = models.CharField(max_length=100)
    name = models.CharField(max_length=100, unique=True)
    quality = models.IntegerField()

    def __str__(self):
        return f"{self.name} * {self.quality}"

class OrderGood(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.PROTECT)
    quality = models.IntegerField()

    def __str__(self):
        return f"{self.order.customer} {self.good.name}*{self.quality}"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    due_date = models.DateField()
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} {self.due_date}"
