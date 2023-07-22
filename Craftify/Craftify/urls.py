"""
URL configuration for Craftify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from CraftifyApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('', views.index),
    path('signin/', views.signin),
    path('contact/', views.contact),
    path('userRegister/', views.userRegister),
    path('artistRegister/', views.artistRegister),
    path('payFees/', views.payFees),
    path('adminViewArtist/', views.adminViewArtist),
    path('artistHome/', views.artistHome),
    path('userHome/', views.userHome),
    path('adminHome/', views.adminHome),
    path('manageRequest/', views.manageRequest),
    path('logout/', views.logout),
    path('profile/', views.profile),
    path('updateProfile/', views.updateProfile),
    path('addItems/', views.addItems),
    path('viewItems/', views.viewItems),
    path('updateProduct/', views.updateProduct),
    path('deleteProduct/', views.deleteProduct),
    path('userViewProduct/', views.userViewProduct),
    path('addToCart/', views.addToCart),
    path('viewCart/', views.viewCart),
    path('paymentForm/', views.paymentForm),
    path('removeFromCart/', views.removeFromCart),
    path('checkOut/', views.checkOut),
    path('viewOrders/', views.viewOrders),
    path('addToWishList/', views.addToWishList),
    path('wishList/', views.wishList),
    path('removeFromWishList/', views.removeFromWishList),
    path('addFeedback/', views.addFeedback),
    path('adminViewProducts/', views.adminViewProducts),
    path('approveProduct/', views.approveProduct),
    path('deleteProduct/', views.deleteProduct),
    path('chat/', views.chat),
]