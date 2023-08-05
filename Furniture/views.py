from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from .forms import NewUserForm, UrbanNestUserForm
from django.contrib.auth import login
from django.contrib import messages
from .forms import FurnitureAdForm
from .models import FurnitureAd, UrbanNestUser, OrderItem, ShoppingCart, Category
from datetime import datetime, timedelta
# from .forms import
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm


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


def register_request(request):
    if request.method == 'POST':
        user_form = NewUserForm(request.POST)
        profile_form = UrbanNestUserForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # Create a shopping cart for the user
            shopping_cart = ShoppingCart.objects.create(buyer=profile)

            return redirect('home')  # Replace 'home' with the URL name for the home page

    else:
        user_form = NewUserForm()
        profile_form = UrbanNestUserForm()

    return render(request, 'main/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"login_form": form})
