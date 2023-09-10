from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='category_img', blank=True)

    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, default="Other", on_delete=models.SET_DEFAULT)
    start_price = models.FloatField()
    current_price = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='product_image', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    buyer = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, related_name="buyer")
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.content}"

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    offer = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.offer}"
