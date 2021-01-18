from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    re_path('^$|^login/$', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('main/', views.main, name='main'),
    path('list/', views.GoodsListView.as_view(), name='list'),
    path('detail/', views.show_goods_detail, name='detail'),
    path('add/', views.add_cart, name='add_cart'),
    path('show_cart/', views.show_cart, name='cart_view'),
    path('submit_orders/', views.submit_orders, name='order_view'),

]