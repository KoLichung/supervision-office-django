from django import forms
from .models import *
  
class ProductImageForm(forms.ModelForm):
  
    class Meta:
        model = ProductImage
        fields = ['product', 'image']