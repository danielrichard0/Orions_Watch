from django.urls import path
from django.conf import settings

from . import views

app_name = "products"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("category/<slug:category_slug>/",views.IndexView.as_view(), name="product-category")
]