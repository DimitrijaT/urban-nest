from django.shortcuts import render, redirect
from .models import FurnitureAd, UrbanNestUser, OrderItem, ShoppingCart
from datetime import datetime, timedelta
# from .forms import
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def index(request):
    # get 8 most viewed ads
    queryset = FurnitureAd.objects.order_by('-views')[:8]
    context = {'popular_ads': queryset}
    return render(request, 'index.html', context=context)


def details(request, pk):
    item = FurnitureAd.objects.get(id=pk)
    context = {'item': item}
    return render(request, 'ad-details.html', context=context)
