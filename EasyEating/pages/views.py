from django.http import HttpResponse
from django.shortcuts import render


def index(req):
    return render(req,"pages/index.html")
def about(req):
    return render(req,"pages/about.html")
def contact(req):
    return render(req,"pages/contact.html")
# Create your views here.
