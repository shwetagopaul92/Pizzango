from django.urls import path

from . import views

urlpatterns = [
    path("menu", views.menu, name="menu"),
    path("category", views.category, name="category"),
    path("options", views.options, name="options"),
    path("cart", views.cart, name="cart"),
    path("order", views.order, name="order"),
    path("sendmail", views.sendmail, name="sendmail"),
    path("adminview", views.adminview, name="adminview"),
    path("orderstatusupdate", views.orderstatusupdate,
         name="orderstatusupdate")
]
