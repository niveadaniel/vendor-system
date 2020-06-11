from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'home-page.html')


def list_vendor(request):
    return render(request, 'list_vendor.html')