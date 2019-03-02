from django import forms
from Inventory.models import Product

class ProductImageUpload(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('image',)