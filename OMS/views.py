from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.views.generic import ListView, View
from django.views.generic.edit import ModelFormMixin

from .models import Good, Order, OrderGood
from .forms import OrderFrom


# Create your views here.
class IndexView(ListView):
    paginate_by = 4

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)

        respond = {
            'page_range': list(range(1, min(context['paginator'].num_pages + 1, 4))),
            'page_obj': {
                'next_page_number': context['page_obj'].next_page_number() if context['page_obj'].has_next() else None,
                'previous_page_number': context['page_obj'].previous_page_number() if context['page_obj'].has_previous() else None,
                'number': context['page_obj'].number,
            },
            'orders': [{'order': str(order), 'id': order.id} for order in context['object_list']]
        }

        return JsonResponse(respond)

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, 'customer'):
            return Order.objects.filter(customer=user.customer, done=False)
        else:
            return Order.objects.filter(done=False).order_by('due_date')

class BaseFormView(ModelFormMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(get_token(request))

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

class GoodsView(PermissionRequiredMixin, ListView):
    permission_required = 'OMS.view_good'

    def get(self, request, *args, **kwargs):
        object_list = [{'good': str(good), 'name': good.name} for good in self.get_context_data(object_list=Good.objects.all())['object_list']]
        return JsonResponse({'goods': object_list})

class GoodsCreationView(PermissionRequiredMixin, BaseFormView):
    permission_required = 'OMS.add_good'
    model = Good
    fields = ['group', 'name', 'quality']

    def form_valid(self, form):
        form.save()
        return JsonResponse({'status': 'success'})

class GoodsDeleteView(PermissionRequiredMixin, View):
    permission_required = 'OMS.delete_good'
    def get(self, request, *args, **kwargs):
        Good.objects.get(name=kwargs['name']).delete()
        return JsonResponse({'status': 'success'})

class GoodsUpdateView(PermissionRequiredMixin, BaseFormView):
    permission_required = 'OMS.change_good'
    model = Good
    fields = ['quality']

    def get(self, request, *args, **kwargs):
        quality = Good.objects.get(name=kwargs['name']).quality
        return JsonResponse({
            'quality': quality,
            'csrfmiddlewaretoken': get_token(request)
        })

    def form_valid(self, form):
        goods = Good.objects.get(name=self.kwargs['name'])
        goods.quality = form.cleaned_data['quality']
        goods.save()
        return JsonResponse({'status': 'success'})

class OrderGoodView(PermissionRequiredMixin, View):
    permission_required = 'OMS.add_order'
    def get(self, request, *args, **kwargs):
        goods = Good.objects.filter(group=kwargs['group'])
        return JsonResponse({'goods': [good.name for good in goods]})

class OrderView(PermissionRequiredMixin, BaseFormView):
    permission_required = 'OMS.add_order'
    form_class = OrderFrom

    def get(self, request, *args, **kwargs):
        group = {good.group for good in Good.objects.all()}

        return JsonResponse({
            'csrfmiddlewaretoken': get_token(request),
            'group': list(group),
            'address': request.user.customer.address,
        })

    def form_valid(self, form):
        return JsonResponse({'status': 'success'})

class OrderDeleteView(PermissionRequiredMixin, View):
    permission_required = 'OMS.delete_order'

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['id'])
        order_goods = OrderGood.objects.filter(order=order)

        for order_good in order_goods:
            good = Good.objects.get(name=order_good.good.name)
            good.quality += order_good.quality
            good.save()

        order.delete()
        return JsonResponse({'status': 'success'})

class OrderUpdateView(PermissionRequiredMixin, View):
    permission_required = 'OMS.change_order'

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['id'])
        order.done = True
        order_goods = OrderGood.objects.filter(order=order)

        for order_good in order_goods:
            order_good.delete()

        order.save()

        return JsonResponse({'status': 'success'})
