from django import forms
from .models import Product, Review, SizeOption
from django.contrib.auth.models import User


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "desc", "image", "spice_level"]


class SizeOptionForm(forms.ModelForm):
    class Meta:
        model = SizeOption
        fields = ["product", "size", "price"]


class ReviewForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Review
        fields = ['user', 'rating', 'content']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].initial = kwargs['initial'].get('user')