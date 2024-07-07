from django.db import models
from django.contrib.auth.models import User

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'user'  # Add this line to specify the username field

    def __str__(self):
        return self.user.username

class Shop(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE)
    profile_image = models.ImageField(default='default.jpg', upload_to='shop_profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set to the current date and time when the object is created
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField()
    image = models.ImageField(default='default.jpg', upload_to='item_images/', null=True, blank=True)

    def __str__(self):
        return self.name
