from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from stores.models import Item, Shop, Vendor

from django.forms.widgets import PasswordInput, TextInput

#create user form
class CreateUserForm(UserCreationForm):
    class Meta:
        model= User
        fields=['username','email','password1','password2']

#user authentication login form

class LoginForm(AuthenticationForm):
    username= forms.CharField(widget=TextInput())
    password= forms.CharField(widget=PasswordInput())


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'stock_quantity', 'image']

class VendorRegistrationForm(forms.ModelForm):
    bio = forms.CharField(max_length=500, required=False)

    class Meta:
        model = Vendor
        fields = ['bio']

class ShopCreationForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'description', 'location', 'profile_image']

