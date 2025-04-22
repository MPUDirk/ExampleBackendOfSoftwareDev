from django.contrib import admin

from .models import Customer, Good, OrderGood, Order

# Register your models here.
admin.site.register(Customer)
admin.site.register(Good)
admin.site.register(OrderGood)
admin.site.register(Order)