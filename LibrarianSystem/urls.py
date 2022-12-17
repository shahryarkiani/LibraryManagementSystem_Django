"""Librarian System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from . import views


urlpatterns = [
    path('', views.manageHome, name='manage-home'),
    path('register/', views.manageRegister, name='manage-register'),
    path('checkout/', views.manageCheckout, name='manage-checkout'),
    path('checkout/api/books/', views.bookListView, name='book-list-view'),
    path('checkout/api/users/', views.userListView, name='user-list-view'),
    path('users/', views.manageUser, name='manage-user'),
    path('users/<pk>/', views.manageUserDetail, name='manage-user-detail'),
    path('users/api/userSearch', views.searchUser, name='manage-user-search')
]
