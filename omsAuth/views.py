import time

from django.contrib.auth import login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import AuthenticationForm
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.views.generic.edit import View, ModelFormMixin

from .forms import OMSUserCreationForm, OMSStaffCreationForm
from OMS.models import Customer


# Create your views here.
class Snowflake:
    timestamp = 1744516800
    sequence = 0
    last_timestamp = 1744516800

    @staticmethod
    def get_id():
        now_timestamp = int(time.time())
        if now_timestamp == Snowflake.last_timestamp:
            Snowflake.sequence = (Snowflake.sequence + 1) & 4095
            if Snowflake.sequence == 0:
                now_timestamp += 1
        else:
            Snowflake.sequence = 0
        Snowflake.last_timestamp = now_timestamp
        return ((now_timestamp - Snowflake.timestamp) << 22) | Snowflake.sequence

class BaseOMSAuthFormView(ModelFormMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(get_token(self.request))

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return JsonResponse({'status': 'fail', 'errors': form.errors}, status=400)

class OMSLoginView(BaseOMSAuthFormView):
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()

        if isinstance(user, User):
            u = {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'isAuthenticated': True,
            }
            respond_data = {'status': 'success', 'user': u}

            if user.is_superuser:
                perms = '__super__'
            elif user.is_staff:
                perms = '__staff__'
            else:
                perms = '__customer__'
            respond_data['perms'] = perms
            respond_data.update({'csrfmiddlewaretoken': get_token(self.request)})

            login(self.request, user)

            return JsonResponse(respond_data, status=200)
        else:
            return JsonResponse({'status': 'fail', 'error': 'Instance not a User'}, status=500)

class OMSSignupView(BaseOMSAuthFormView):
    form_class = OMSUserCreationForm

    def form_valid(self, form):
        data = form.cleaned_data

        try:
            user = User.objects.create_user(
                username=data['username'],
                password=data['password1'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
            )
            user.groups.add(Group.objects.get(name='Customer'))

            Customer.objects.create(
                user=user,
                address=form.data['address'],
            )

            return JsonResponse({'status': 'success', 'username': user.username}, status=200)
        except KeyError:
            form.add_error('address', 'This field is required')
            return self.form_invalid(form)
        except Exception as e:
            return JsonResponse({'status': 'fail', 'error': str(e)}, status=500)

class OMSAddStaffView(PermissionRequiredMixin, BaseOMSAuthFormView):
    permission_required = 'auth.add_user'
    form_class = OMSStaffCreationForm

    def form_valid(self, form):
        data = form.cleaned_data

        try:
            user = User.objects.create_user(
                username=str(Snowflake.get_id()),
                password=data['password1'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                is_staff=True,
            )
            user.groups.add(Group.objects.get(name='Staff'))

            return JsonResponse({'status': 'success', 'username': user.username}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'fail', 'error': str(e)}, status=500)

class OMSLogoutView(BaseOMSAuthFormView):
    def get(self, request, *args, **kwargs):
        logout(self.request)
        return JsonResponse({'status': 'success'}, status=200)

class UserPermsView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            perms = '__super__'
        elif request.user.is_staff:
            perms = '__staff__'
        else:
            perms = '__customer__'

        return JsonResponse({'status': 'success', 'perms': perms}, status=200)

class OMSUsersView(PermissionRequiredMixin, View):
    permission_required = 'auth.change_user'

    @staticmethod
    def user_to_dict(user):
        return {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }

    def get(self, request, *args, **kwargs):
        users = {
            'staffs': [self.user_to_dict(staff) for staff in User.objects.filter(is_staff=True, is_superuser=False)],
        }

        return JsonResponse(users)

class OMSUserDeleteView(PermissionRequiredMixin, View):
    permission_required = 'auth.delete_user'

    def get(self, request, *args, **kwargs):
        User.objects.get(username=kwargs['username']).delete()
        return JsonResponse({'status': 'success'}, status=200)
