from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, SetPasswordForm
from .models import User, Profile
from django.forms import ModelForm


class MyUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter username'}),
        label=''
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter first name'}),
        label=''
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter last name'}),
        label=''
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter email'}),
        label=''
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
        label=''
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        label=''
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        label=''
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')

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


class Profileform(ModelForm):
    class Meta:
        model = Profile
        fields = ["username", "first_name", "last_name", "profile_picture"]