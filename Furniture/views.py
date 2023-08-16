from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewUserForm, UrbanNestUserForm
from django.contrib.auth import login
from django.contrib import messages
from .forms import FurnitureAdForm
from .models import FurnitureAd, UrbanNestUser, Product, ShoppingCart, Category, Testimonial, FrontCover, About, Contact
from datetime import datetime, timedelta
# from .forms import
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
def index(request):
    # get 8 most viewed ads
    queryset = FurnitureAd.objects.filter(active=True).order_by('-views')[:8]
    testimonials = Testimonial.objects.all()
    front_cover = FrontCover.objects.get(active=True)
    context = {'popular_ads': queryset, 'testimonials': testimonials, 'front_cover': front_cover}
    return render(request, 'index.html', context=context)


def about(request):
    about_obj = About.objects.latest('creation_date')  # Assuming you want the latest about entry
    context = {'about': about_obj}
    return render(request, 'about.html', context=context)


def contact(request):
    if request.method == 'POST':
        user = UrbanNestUser.objects.get(user=request.user)
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        Contact.objects.create(user=user, name=name, email=email, message=message)
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


def adlist(request, pk):
    category = get_object_or_404(Category, pk=pk)
    search_query = request.GET.get('search_query', '')
    page = request.GET.get('page')

    # Filter furniture ads by category and search query
    furniture_ads = FurnitureAd.objects.filter(category=category, active=True)
    if search_query:
        furniture_ads = furniture_ads.filter(name__icontains=search_query)

    items_per_page = 4
    paginator = Paginator(furniture_ads, items_per_page)

    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    context = {
        'furniture_ads': page,
        'category': category,
        'search_query': search_query,
    }

    return render(request, 'ad-list.html', context=context)


@login_required
def add_furniture_ad(request):
    if request.method == 'POST':
        form = FurnitureAdForm(request.POST, request.FILES)
        if form.is_valid():
            furniture_ad = form.save(commit=False)
            furniture_ad.seller = UrbanNestUser.objects.get(user=request.user)
            # if no photo
            if not request.FILES:
                furniture_ad.image = 'images/furnitures/default.jpg'
            furniture_ad.save()
            return redirect(dashboard_home)
    else:
        form = FurnitureAdForm()
    user = UrbanNestUser.objects.get(user=request.user)
    context = {'form': form, 'user': user}
    return render(request, 'ad-add.html', context=context)


@login_required
def delete_furniture_ad(request, ad_id):
    ad = get_object_or_404(FurnitureAd, id=ad_id)

    if ad.seller.user != request.user and ad.visible is True:
        # Redirect or show an error message if the logged-in user is not the ad's seller
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    ad.delete()
    return redirect(dashboard_home)


@login_required
def edit_furniture_ad(request, ad_id):
    ad = get_object_or_404(FurnitureAd, id=ad_id)

    if ad.seller.user != request.user:
        # Redirect or show an error message if the logged-in user is not the ad's seller
        return redirect(dashboard_home)

    if request.method == 'POST':
        form = FurnitureAdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form = form.save(commit=False)
            if not request.FILES:
                form.image = 'images/furnitures/default.jpg'
            form.save()
            return redirect(dashboard_home)
    else:
        form = FurnitureAdForm(instance=ad)

    user = ad.seller
    context = {'form': form, 'user': user}
    return render(request, 'ad-edit.html', context=context)


def register_request(request):
    if request.method == 'POST':
        user_form = NewUserForm(request.POST)
        profile_form = UrbanNestUserForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'photo' in request.FILES:
                profile.photo = request.FILES['photo']
            else:
                profile.photo = 'images/users/default.jpg'
            profile.save()
            # Create a shopping cart for the user
            profile_shopping_cart = ShoppingCart.objects.create(buyer=profile)
            profile_shopping_cart.save()
            profile.shopping_cart = profile_shopping_cart
            profile.save()

            return redirect('/')

    else:
        user_form = NewUserForm()
        profile_form = UrbanNestUserForm()

    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def edit_settings(request):
    user_settings = UrbanNestUser.objects.get(user=request.user)

    if request.method == 'POST':
        form = UrbanNestUserForm(request.POST, request.FILES, instance=user_settings)

        if form.is_valid():
            form = form.save(commit=False)
            if not request.FILES:
                form.photo = 'images/users/default.jpg'
            form.save()

            return redirect(dashboard_home)
    else:
        form = UrbanNestUserForm(instance=user_settings)

    user = UrbanNestUser.objects.get(user=request.user)
    context = {'form': form, 'user': user}
    return render(request, 'registration/edit_settings.html', context=context)


@login_required
def dashboard_home(request):
    # get the user
    user = UrbanNestUser.objects.get(user=request.user)
    list_of_ads = FurnitureAd.objects.filter(seller=user).order_by('-creation_date')
    context = {'user': user, 'list_of_ads': list_of_ads}
    return render(request, 'dashboard/dashboard-home.html', context=context)


@login_required
def dashboard_report(request):
    # get the user
    user = UrbanNestUser.objects.get(user=request.user)
    context = {'user': user}
    return render(request, 'dashboard/dashboard-report.html', context=context)


@login_required
def dashboard_messages(request):
    # get the user
    user = UrbanNestUser.objects.get(user=request.user)
    context = {'user': user}
    return render(request, 'dashboard/dashboard-messages.html', context=context)


@login_required
def offers(request):
    # get the user
    user = UrbanNestUser.objects.get(user=request.user)
    offers = Product.objects.filter(furniture__seller=user).exclude(status='IC').order_by('-creation_date')
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
    list_of_orders.order_by('-creation_date')
    print(products)
    context = {'user': user, 'list_of_orders': list_of_orders}
    return render(request, 'dashboard/dashboard-my-orders.html', context=context)


@login_required
def shopping_cart(request):
    # get the user
    user = UrbanNestUser.objects.get(user=request.user)
    user_shopping_cart = user.shopping_cart
    if user_shopping_cart is not None:
        items = user_shopping_cart.items.all()
        context = {'shopping_cart': user_shopping_cart, 'items': items}
    else:
        context = {'shopping_cart': user_shopping_cart}
    return render(request, 'shopping-cart.html', context=context)


@login_required
def add_to_cart(request, furniture_id):
    furniture = get_object_or_404(FurnitureAd, id=furniture_id)
    user = UrbanNestUser.objects.get(user=request.user)
    if furniture.seller == user:
        return HttpResponseRedirect(request.POST.get('next', '/'))
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
