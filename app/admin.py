from django.contrib import admin
from .models import Category, Notification, History, Product, ProfilePic
# Register your models here.

admin.site.register(Category)
admin.site.register(Notification)
admin.site.register(History)
admin.site.register(ProfilePic)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('date_added','id','name','category','quantity')