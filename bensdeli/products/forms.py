from django import forms
from .models import Product, Review
from django.contrib.auth.models import User


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "desc", "image", "price", "spice_level"]


class ReviewForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Review
        fields = ['user', 'rating', 'content']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].initial = kwargs['initial'].get('user')