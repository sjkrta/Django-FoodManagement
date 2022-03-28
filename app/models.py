from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.
class Notification(models.Model):
    content = models.CharField(max_length=250)
    time_stamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.content

class History(models.Model):
    content = models.CharField(max_length=250)
    time_stamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'History'

    def __str__(self):
        return self.content

class Category(models.Model):
    name    = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class Product(models.Model):
    name            = models.CharField(max_length=50, unique=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity        = models.IntegerField()
    inventory_size = models.IntegerField(default=0)
    image           = models.ImageField(upload_to='products')
    description     = models.TextField(max_length=2000)
    date_added      = models.DateTimeField()
    notify_quantity = models.IntegerField()
    notify_by       = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class DateInput(forms.DateInput):
    input_type = 'date'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'date_added':DateInput()
        }

class ProfilePic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='accounts', default='accounts/default.jpg')

    def __str__(self):
        return self.user.username

class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = ProfilePic
        fields = ['image']