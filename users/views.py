from django.contrib.auth import authenticate
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})
    context = {
        "user": request.user
    }
    return render(request, "users/user.html", context)


# To render the homepage for the website
def homepage(request):
    return render(request, "users/homepage.html")


# To allow users to register for using the website
def register(request):
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    username = request.POST["username"]
    password = request.POST["password"]
    email = request.POST["email"]
    user = User.objects.create_user(username=username, email=email,
                                    password=password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    context = {
            "user": request.user
    }
    return render(request, "users/login.html")


# To allow user to login to use the website
def login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        django_login(request, user)
        return HttpResponseRedirect(reverse("menu"))
    else:
        return render(request, "users/login.html",
                      {"message": "Invalid credentials."})


# To allow users to logout of website
def logout(request):
    django_logout(request)
    return render(request, "users/login.html",
                  {"message": "You are now logged out."})
