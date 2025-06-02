from django.shortcuts import render
from .models import Item, Order, Topping, Addon
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError


# To show the items on the menu
def menu(request):
    context = {
        "items": Item.objects.all(),
        "addons": Addon.objects.all(),
        "toppings": Topping.objects.all()
    }
    return render(request, "menu/menu.html", context)


# To show the menu items by their category like Pasta,Salads, etc.
def category(request):
    context = {
        "category": list(Item.objects.order_by().values_list('category',
                         flat=True).distinct())
    }
    return render(request, "order/category.html", context)


# To show the options of menu items under a specific category
def options(request):
    selected_category = request.POST["category"]
    choices = Item.objects.filter(category=selected_category)
    # To display the options specific to the category chosen by the user
    if selected_category == "Regular Pizza" or selected_category == "Sicilian Pizza":
        context = {
            "name": list(choices.order_by().values_list('name', flat=True).distinct()),
            "size": list(choices.order_by().values_list('size', flat=True).distinct()),
            "type": list(choices.order_by().values_list('type', flat=True).distinct()),
            "price": list(choices.order_by().values_list('price', flat=True).distinct()),
            "toppings": Topping.objects.all()
        }
    elif selected_category == "Subs":
        context = {
            "name": list(choices.order_by().values_list('name', flat=True).distinct()),
            "size": list(choices.order_by().values_list('size', flat=True).distinct()),
            "type": list(choices.order_by().values_list('type', flat=True).distinct()),
            "price": list(choices.order_by().values_list('price', flat=True).distinct()),
            "addons": Addon.objects.all()
        }
    else:
        context = {
            "name": list(choices.order_by().values_list('name', flat=True).distinct()),
            "size": list(choices.order_by().values_list('size', flat=True).distinct()),
            "type": list(choices.order_by().values_list('type', flat=True).distinct()),
            "price": list(choices.order_by().values_list('price', flat=True).distinct()),
        }
    return render(request, "order/options.html", context)


# To show the user the item they selected and to update database with order_status being "Pending, items is still in cart"
def cart(request):
    selected_name = request.POST["name"]
    selected_size = request.POST["size"]
    selected_type = request.POST["type"]
    selected_toppings = request.POST.getlist('toppings')
    subsetchoice = Item.objects.filter(name=selected_name)
    result = subsetchoice.filter(size=selected_size, type=selected_type)
    for value in result:
        decimal_price = value.price
    price = str(decimal_price)
    selected_addons = request.POST.getlist('addons')
    # To check if add on exists , if it does get the subset values for the addon
    if len(selected_addons) > 0:
        subsetaddons = Addon.objects.filter(addons_name__in=selected_addons)
        print(subsetaddons)
        price_addon = []
        for val in subsetaddons:
            price_addon.append(str(val.addons_price))
        res = list(map(float, price_addon))
        total_addonprice = sum(res)
    else:
        price_addon = 0
        total_addonprice = 0
    context = {
     "name": selected_name,
     "type": selected_type,
     "size": selected_size,
     "price": price,
     "addons_price": price_addon,
     "addons": selected_addons,
     "topping": selected_toppings
    }
    # To get the username of the current user
    user = User.objects.get(username=request.user.username)
    username = user.username
    # To add to Order model
    order_new = Order()
    order_new.name = selected_name
    order_new.type = selected_type
    order_new.size = selected_size
    order_new.price = decimal_price
    order_new.user_name = username
    order_new.toppings = selected_toppings
    order_new.addons = selected_addons
    order_new.addons_price = total_addonprice
    order_new.order_status = "Pending, items is still in cart"
    order_new.save()
    return render(request, "order/cart.html", context)


# To show the final order with total bill amount and confirm a order
def order(request):
    user = User.objects.get(username=request.user.username)
    username = user.username
    subsetchoice = Order.objects.filter(user_name=username)
    name = list(subsetchoice.order_by().values_list('name', flat=True))
    price = list(subsetchoice.order_by().values_list('price', flat=True))
    addon_price = list(subsetchoice.order_by().values_list('addons_price', flat=True))
    # To calculate total bill cost
    total_price = str(sum(price))
    total_addon_price = str(sum(addon_price))
    t1 = float(total_price)
    t2 = float(total_addon_price)
    total_bill = t1+t2
    context = {
     "name": name,
     "total_bill": total_bill,
    }
    return render(request, "order/order.html", context)


# To update the status of the order from "Pending. items still in cart" to "Order Placed"
def orderstatusupdate(request):
    user = User.objects.get(username=request.user.username)
    username = user.username
    currentuser_orders = Order.objects.filter(user_name=username)
    currentuser_orders.update(order_status="Order Placed")
    return render(request, "order/ordercompleted.html")


# To allow only the admin to view a page with all the order details with their latest status
@login_required
def adminview(request):
    context = {
        "username": request.user.username,
        "orders": Order.objects.all()
    }
    return render(request, "order/adminorderview.html", context)


def sendmail(request):
    user = User.objects.get(username=request.user.username)
    user_email = user.email
    send_mail('Order confirmation from PIZZA', 'Hi, your order has been placed. This is a confirmation email!',
              settings.EMAIL_HOST_USER, [user_email], fail_silently=False)
    return render(request, "order/sendemail.html")
