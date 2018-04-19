"""circinus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='index'),
    # product
    path('product/create/', views.ProductCreate.as_view(), name='product-create'),
    path('product/list/', views.ProductList.as_view(), name='product-list'),
    path('product/detail/<pk>/', views.ProductDetail.as_view(), name='product-detail'),
    path('product/update/<pk>/', views.ProductUpdate.as_view(), name='product-update'),
    path('product/delete/<pk>/', views.ProductDelete.as_view(), name='product-delete'),
    # provider
    path('provider/create/', views.ProviderCreate.as_view(), name='provider-create'),
    path('provider/list/', views.ProviderList.as_view(), name='provider-list'),
    path('provider/detail/<pk>/', views.ProviderDetail.as_view(), name='provider-detail'),
    path('provider/update/<pk>/', views.ProviderUpdate.as_view(), name='provider-update'),
    path('provider/delete/<pk>/', views.ProviderDelete.as_view(), name='provider-delete'),
    # entry
    path('entry/create/', views.EntryCreate.as_view(), name='entry-create'),
    path('entry/list/', views.EntryList.as_view(), name='entry-list'),
    path('entry/detail/<pk>/', views.EntryDetail.as_view(), name='entry-detail'),
    # path('entry/update/<pk>/', views.EntryUpdate.as_view(), name='entry-update'),
    path('entry/delete/<pk>/', views.EntryDelete.as_view(), name='entry-delete'),

    path('entry/csv/<pk>/', views.some_view, name='entry-csv')
]
