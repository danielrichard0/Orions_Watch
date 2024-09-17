"""
URL configuration for fetishiastore01 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("products/", include("products.urls")),
    path('cart/', include("cart.urls")),
    path('customers/', include("customers.urls")),
    path('login/', views.custom_login_view, name="user-auth" ),
    path('registration', views.custom_registration_view, name='user-registration'),
    path('admin/', admin.site.urls, name="admin-site"),
    path('logout/', views.logout_view, name='logout')
    
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
