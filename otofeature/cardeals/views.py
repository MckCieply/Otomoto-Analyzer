from django.shortcuts import render
from django.http import HttpResponse
from .models import Cars
# Create your views here.

#def index(response):
#    return render(response, "cardeals/base.html", {})

def home(response):
    return render(response, "cardeals/home.html")

def roccodeals(response):
    deals = Cars.objects.all()
    return render(response, "cardeals/rocco.html", {'deals': deals})

def lancerdeals(response):
    return render(response, "cardeals/lancer.html", {})

#{% extends 'cardeals/base.html' %}
#to extend base template