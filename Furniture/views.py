from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from .forms import FurnitureAdForm
from .models import FurnitureAd, UrbanNestUser, OrderItem, ShoppingCart, Category
from datetime import datetime, timedelta
# from .forms import
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def index(request):
    # get 8 most viewed ads
    queryset = FurnitureAd.objects.order_by('-views')[:8]
    context = {'popular_ads': queryset}
    return render(request, 'index.html', context=context)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def details(request, pk):
    item = FurnitureAd.objects.get(id=pk)
    context = {'item': item}

    # Increase the views count when the view is opened
    item.views += 1
    item.save()

    return render(request, 'ad-details.html', context=context)


def category(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'ad-category.html', context=context)


def adlist(request, pk, page=1):
    # Get all furniture ads for the specified category
    furniture_ads = FurnitureAd.objects.filter(category__pk=pk)

    print(furniture_ads)
    # Number of ads to display per page
    items_per_page = 10

    # Create a Paginator instance
    paginator = Paginator(furniture_ads, items_per_page)

    try:
        # Get the specified page from the paginator
        page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        page = paginator.page(paginator.num_pages)

    context = {
        'furniture_ads': page,
    }

    return render(request, 'ad-list.html', context=context)


@login_required
def add_furniture_ad(request):
    if request.method == 'POST':
        form = FurnitureAdForm(request.POST, request.FILES)
        if form.is_valid():
            furniture_ad = form.save(commit=False)
            furniture_ad.seller = UrbanNestUser.objects.get(user=request.user)

            furniture_ad.save()
            return redirect('index')
    else:
        form = FurnitureAdForm()
    context = {'form': form}
    return render(request, 'ad-add.html', context=context)
