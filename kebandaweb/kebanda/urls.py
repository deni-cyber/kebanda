from django.urls import path
from . import views


app_name = "kebanda"
urlpatterns = [
    # ex: /polls/
    path("", views.landingPage, name="landingPage"),
    path("signup/", views.signup, name="signupPage"),
    path("login/", views.login, name="loginPage"),
    path("profile/", views.profile, name="profilePage"),
    path("logout/", views.logout, name="logout"),
    path("myshop/", views.myshop, name="myshop"),
    path("myduka/", views.myduka, name="myduka"),
    path('add_item/', views.add_item, name='add_item'),
    path('vendor-registration/', views.vendor_registration, name='vendor_registration'),
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
         ]

