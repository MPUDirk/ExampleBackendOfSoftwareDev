from datetime import timedelta, datetime

from django import forms
from django.contrib.auth.models import User

from .models import Order, OrderGood, Good, Customer


class OrderFrom(forms.Form):
    due_date = forms.DateField()
    username = forms.CharField(max_length=100)

    def clean_due_date(self):
        data = self.cleaned_data['due_date']
        if data - timedelta(days=3) <= datetime.now().date():
            raise forms.ValidationError('The delivery due date date is at least three days')
        return data

    def clean(self):
        data = self.data
        orders = dict()

        customer = Customer.objects.get(user=User.objects.get(username=data['username']))

        for k in data:
            if k in ['csrfmiddlewaretoken', 'username', 'due_date']:
                continue
            orders.setdefault(k[-1], dict())[k[:-1]] = data[k]

        order = Order.objects.create(customer=customer, due_date=data['due_date'])

        try:
            for o in orders.values():
                good = Good.objects.get(name=o['name'])
                if good.quality < int(o['quality']):
                    raise forms.ValidationError(f'No enough {good.name}')
                good.quality -= int(o['quality'])
                good.save()
                OrderGood.objects.create(order=order, good=good, quality=o['quality'])
        except Exception as e:
            order.delete()
            raise forms.ValidationError(e)