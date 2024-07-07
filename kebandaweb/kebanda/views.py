from django.shortcuts import render,redirect, get_object_or_404, Http404
from .forms import CreateUserForm, LoginForm, ItemForm, VendorRegistrationForm, ShopCreationForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from . models import Profile
from stores.models import Item, Shop, Vendor
from django.contrib.auth.forms import AuthenticationForm


def landingPage(request):
    items=Item.objects.all()
    context= {'items': items}
    return render( request, "kebanda/index.html", context=context)

def signup(request):
    form=CreateUserForm()
    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            user_profile=Profile(user=user)
            user_profile.save()
            return redirect("/kebanda/login/")
        
    context={'signupform':form}
    return render(request,"kebanda/signup.html",context= context)

def login(request):
    form= LoginForm()

    if request.method =='POST':
        form =LoginForm(request, data=request.POST)

        if form.is_valid():

            username=request.POST.get('username')
            password=request.POST.get('password')

            user = authenticate(request, username=username, password= password)

            if user is not None:
                auth.login(request, user)
                context={'username':username}
            
                return redirect('/kebanda/profile/')
            
    context={'loginform':form}
    return render(request, "Kebanda/login.html",context=context)

@login_required(login_url='/kebanda/login/')
def profile(request):
    user= request.user
    try:
        person = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        raise Http404("No Profile matches the given query.")
    context={'user': user, 'person': person}
    return render(request, 'kebanda/profile.html', context= context)


@login_required(login_url='/kebanda/login/')
def logout(request):
    auth.logout(request)
    return redirect('/kebanda/login/')

@login_required(login_url='/kebanda/login/')
def myshop(request):
    if request.user.is_authenticated:
        # Retrieve the related shop for the current user
        try:
            user_shop = request.user.vendor.shop
            user_items=Item.objects.filter(shop__vendor__user=request.user)
        except Shop.DoesNotExist:
            user_shop = None
        
        return render(request, 'kebanda/myshopsprofile.html', {'user_shop': user_shop,
                                                               'user_items': user_items})
    else:
        # Redirect or handle the case when the user is not authenticated
        return redirect('login') 
    

@login_required(login_url='/kebanda/login/')
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            # Set the shop field to the user's shop
            form.instance.shop = request.user.vendor.shop
            form.save()
            return redirect('/kebanda/myshop/')  # Redirect to a success page or the item list
    else:
        form = ItemForm()

    return render(request, 'kebanda/additem.html', {'form': form})


@login_required
def vendor_registration(request):
    user = request.user  # Get the current logged-in user

    if request.method == 'POST':
        vendor_form = VendorRegistrationForm(request.POST)
        auth_form = AuthenticationForm(request, data=request.POST)
        shop_form = ShopCreationForm(request.POST, request.FILES)

        if vendor_form.is_valid() and auth_form.is_valid() and shop_form.is_valid():
            # Authenticate user with provided password
            authenticated_user = auth_form.get_user()

            if authenticated_user == user:
                # Create a vendor associated with the user
                vendor = Vendor.objects.create(user=user, bio=vendor_form.cleaned_data['bio'])

                # Create a shop associated with the vendor
                shop = shop_form.save(commit=False)
                shop.vendor = vendor
                shop.save()

                return redirect('/kebanda/myshop/')  # Redirect to a success page
    else:
        vendor_form = VendorRegistrationForm()
        auth_form = AuthenticationForm()
        shop_form = ShopCreationForm()

    return render(request, 'kebanda/vendor_registration.html', {'vendor_form': vendor_form, 'auth_form': auth_form, 'shop_form': shop_form})


@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            # Redirect to the item detail page or the shop's dashboard
            return redirect('/kebanda/myshop/')  # Update with your actual dashboard URL
    else:
        form = ItemForm(instance=item)
    return render(request, 'kebanda/edititem.html', {'form': form, 'item': item})

@login_required
def myduka(request):
    if request.user.is_authenticated:
        # Retrieve the related shop for the current user
        try:
            user_items=Item.objects.filter(shop__vendor__user=request.user)
        except Shop.DoesNotExist:
            user_shop = None
        
        return render(request, 'kebanda/myduka.html', {'user_items': user_items})
    else:
        # Redirect or handle the case when the user is not authenticated
        return redirect('login') 
