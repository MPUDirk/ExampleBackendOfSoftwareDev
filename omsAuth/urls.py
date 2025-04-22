from django.urls import path

from . import views


urlpatterns = [
    path('', views.OMSUsersView.as_view(), name='home'),
    path('perms/', views.UserPermsView.as_view(), name='perms'),
    path('<int:username>/del/', views.OMSUserDeleteView.as_view(), name='delete'),

    path('login/', views.OMSLoginView.as_view(), name='login'),
    path('logout/', views.OMSLogoutView.as_view(), name='logout'),
    path('signup/', views.OMSSignupView.as_view(), name='signup'),
    path('staff/new/', views.OMSAddStaffView.as_view(), name='new_staff')
]
