from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm



class RegisterForm(UserCreationForm):
    username = forms.CharField(help_text='')
    email = forms.EmailField(help_text='')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password', help_text='')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm password', help_text='')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class UserEditForm(forms.ModelForm):
    username = forms.CharField(help_text='')
    class Meta:
        model = User
        fields = ["username", "email"]


class CustomPasswordResetForm(PasswordResetForm):
    # Customize the form fields or behavior here
    pass