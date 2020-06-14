"""vendorapp URL Configuration

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
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('login/submit', views.submit_login),
    path('logout/', views.submit_logout, name='submit_logout'),
    path('list/vendor/', views.list_vendor, name='list_vendor'),
    path('edit/vendor/', views.edit_vendor, name='edit_vendor'),
    path('save/vendor/', views.save_vendor, name='save_vendor'),
    path('api/list_vendor/', views.get_vendor_list, name='get_vendor_list'),
    path('delete/vendor/', views.delete_vendor, name='delete_vendor'),
    path('api/delete_vendor/', views.action_delete_vendor, name='action_delete_vendor'),
    path('list/products/', views.list_products, name='list_products'),
    path('api/list_products/', views.get_list_products, name='get_list_products'),
    path('edit/product/', views.edit_product, name='edit_product'),
    path('api/get_vendor_data/<int:vendor_id>/', views.get_vendor_data, name='get_vendor_data'),
    path('save/product/', views.save_product, name='save_product'),
    path('delete/product/', views.delete_product, name='delete_product'),
    path('api/delete_product/', views.action_delete_product, name='action_delete_product')
]
