from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewUserForm, UrbanNestUserForm
from django.contrib.auth import login
from django.contrib import messages
from .forms import FurnitureAdForm
from .models import FurnitureAd, UrbanNestUser, Product, ShoppingCart, Category
from datetime import datetime, timedelta
# from .forms import
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
def index(request):
    # get 8 most viewed ads
    queryset = FurnitureAd.objects.filter(active=True).order_by('-views')[:8]
    context = {'popular_ads': queryset}
    return render(request, 'index.html', context=context)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def details(request, pk):
    if request.method == 'POST':
        user = UrbanNestUser.objects.get(user=request.user)
        user.shopping_cart.add_item(pk)

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
    furniture_ads = FurnitureAd.objects.filter(category__pk=pk, active=True)
    category = Category.objects.get(pk=pk)

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
        'category': category,
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
    user = UrbanNestUser.objects.get(user=request.user)
    context = {'form': form, 'user': user}
    return render(request, 'ad-add.html', context=context)


def register_request(request):
    if request.method == 'POST':
        user_form = NewUserForm(request.POST)
        profile_form = UrbanNestUserForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            print(request.FILES)
            print(request.FILES['photo'])
            profile.photo = request.FILES['photo']
            # Create a shopping cart for the user
            profile_shopping_cart = ShoppingCart.objects.create(buyer=profile)
            profile.shopping_cart = profile_shopping_cart
            profile.save()

            return redirect('home')  # Replace 'home' with the URL name for the home page

    else:
        user_form = NewUserForm()
        profile_form = UrbanNestUserForm()

    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def dashboard_home(request):
    # get the user
    user = UrbanNestUser.objects.get(user=request.user)
    list_of_ads = FurnitureAd.objects.filter(seller=user)
    context = {'user': user, 'list_of_ads': list_of_ads}
    return render(request, 'dashboard/dashboard-home.html', context=context)


@login_required
def offers(request):
    # get the user
    user = UrbanNestUser.objects.get(user=request.user)
    offers = Product.objects.filter(furniture__seller=user).exclude(status='IC')
    context = {'user': user, 'offers': offers}
    return render(request, 'dashboard/dashboard-offers.html', context=context)


@login_required
def offer_accept(request, product_id):
    # get the user
    user = UrbanNestUser.objects.get(user=request.user)
    offer = Product.objects.get(id=product_id)
    offer.status = 'AC'
    offer.furniture.active = False
    offer.furniture.save()
    offer.save()
    user_offers = Product.objects.filter(furniture__seller=user, status='PE', furniture__pk=offer.furniture.pk)
    print(user_offers)
    for o in user_offers:
        if o.pk != offer.pk:
            o.status = 'CA'
            o.save()

    return redirect('offers')


@login_required
def offer_decline(request, product_id):
    # get the user
    user = UrbanNestUser.objects.get(user=request.user)
    offer = Product.objects.get(id=product_id)
    offer.status = 'RE'
    offer.save()
    return redirect('offers')


@login_required
def my_orders(request):
    # get the user
    user = UrbanNestUser.objects.get(user=request.user)
    products = Product.objects.filter(buyer=user)
    list_of_orders = products.filter(status='PE') | products.filter(status='AC') | products.filter(status='RE')
    print(products)
    context = {'user': user, 'list_of_orders': list_of_orders}
    return render(request, 'dashboard/dashboard-my-orders.html', context=context)


@login_required
def shopping_cart(request):
    # get the user
    user = UrbanNestUser.objects.get(user=request.user)
    user_shopping_cart = user.shopping_cart
    items = user_shopping_cart.items.all()
    context = {'shopping_cart': user_shopping_cart, 'items': items}
    return render(request, 'shopping-cart.html', context=context)


@login_required
def add_to_cart(request, furniture_id):
    furniture = get_object_or_404(FurnitureAd, id=furniture_id)
    user = UrbanNestUser.objects.get(user=request.user)
    if furniture.seller == user:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    product = Product.objects.create(buyer=user, furniture=furniture)
    cart, created = ShoppingCart.objects.get_or_create(buyer=user)
    cart.items.add(product)
    return redirect('shopping_cart')


@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = UrbanNestUser.objects.get(user=request.user)
    cart = ShoppingCart.objects.get(buyer=user)
    cart.items.remove(product.pk)
    product.delete()
    return redirect('shopping_cart')


@login_required
def checkout(request):
    user = UrbanNestUser.objects.get(user=request.user)
    cart = ShoppingCart.objects.get(buyer=user)
    items = cart.items.all()
    for item in items:
        item.status = 'PE'
        item.save()
    cart.items.clear()
    return redirect('shopping_cart')
