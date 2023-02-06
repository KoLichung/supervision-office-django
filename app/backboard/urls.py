from django.urls import path, include
from . import views
from django.shortcuts import render
from django.http import HttpResponse 
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # path('index', views.index, name = 'index'), 
    path('customers', views.customers, name = 'customers'), 
    path('customer_detail', views.customer_detail, name = 'customer_detail'),
    path('order_detail', views.order_detail, name = 'order_detail'), 
    path('orders', views.orders, name = 'orders'), 

    path('products', views.products, name = 'products'),
    path('add_new_product', views.add_new_product, name = 'add_new_product'),
    path('edit_product', views.edit_product, name = 'edit_product'),

    #監外商品功能
    path('outside_products', views.outside_products, name = 'outside_products'),
    path('add_new_outside_product', views.add_new_outside_product, name = 'add_new_outside_product'),
    path('edit_outside_product', views.edit_outside_product, name = 'edit_outside_product'),

    path('meals', views.meals, name = 'meals'),
    path('add_new_meal', views.add_new_meal, name = 'add_new_meal'),
    path('edit_meal', views.edit_meal, name = 'edit_meal'),
    
    path('all_categories', views.all_categories, name = 'all_categories'),
    path('new_edit_category', views.new_edit_category, name = 'new_edit_category'),

    #監外商品類別
    path('all_outside_categories', views.all_outside_categories, name = 'all_outside_categories'),
    path('new_edit_outside_category', views.new_edit_outside_category, name = 'new_edit_outside_category'),

    path('offices_order', views.offices_order, name = 'offices_order'), 
    path('bills', views.bills, name = 'bills'), 
    # path('edit_product/<str:id>/delete/', views.deleteImage, name='delete_images'),
    path('', views.login, name='login'),
    path('logout', views.logout, name='logout')
]