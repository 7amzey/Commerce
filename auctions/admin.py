from django.contrib import admin
from .models import User, Category, Product, Comment, Bid

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "start_price", "category", "user", "buyer")
    filter_horizontal = ("watchers", )

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "content", "product", "created_at")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "offer", "product", "created_at")

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
