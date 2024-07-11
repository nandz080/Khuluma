from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, SetPasswordForm
from .models import User

class MyUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter first_name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter last_name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter email'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter phone_number'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter password'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Confirm password'}))
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name','email', 'phone_number', 'profile_picture')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already in use.')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('Phone number already in use.')
        return phone_number

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'email', 'phone_number', 'profile_picture')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already in use.')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('Phone number already in use.')
        return phone_number

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput)

