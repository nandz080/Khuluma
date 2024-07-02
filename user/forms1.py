from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, SetPasswordForm
from .models import User

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone_number', 'profile_picture')

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'email', 'phone_number', 'profile_picture')

class MyPasswordResetForm(PasswordResetForm):
    class Meta(PasswordResetForm.Meta):
        model = User
        fields = ('email',)

class MySetPasswordForm(SetPasswordForm):
    class Meta(SetPasswordForm.Meta):
        model = User
        fields = ('new_password1', 'new_password2')