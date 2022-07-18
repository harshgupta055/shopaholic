from pyexpat import model
from django import forms
from django.forms import ModelForm
from appUser.models import Product, ProductImage, Order
from django import forms


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "about", "price", "category", "quantity", "image"]


class AddProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        fields = '__all__'

