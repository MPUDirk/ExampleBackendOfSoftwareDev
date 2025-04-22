from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('goods/', views.GoodsView.as_view(), name='goods'),
    path('goods/new/', views.GoodsCreationView.as_view(), name='new_goods'),
    path('goods/<slug:name>/del/', views.GoodsDeleteView.as_view(), name='del_goods'),
    path('goods/<slug:name>/edit/', views.GoodsUpdateView.as_view(), name='edit_goods'),
    path('order/', views.OrderView.as_view(), name='order'),
    path('order/<slug:group>/', views.OrderGoodView.as_view(), name='order_good'),
    path('order/<int:id>/del/', views.OrderDeleteView.as_view(), name='del_order'),
    path('order/<int:id>/done/', views.OrderUpdateView.as_view(), name='done_order'),
]