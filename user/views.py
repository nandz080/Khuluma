from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm, MyPasswordResetForm, MySetPasswordForm
from allauth.account.utils import complete_signup
from allauth.account import app_settings
from django.urls import reverse_lazy

def home(request):
    return render(request, 'user/home.html')

def signup(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)  # Log in the user after signup
            complete_signup(request, user, app_settings.EMAIL_VERIFICATION, None)
            return redirect(reverse_lazy('my_messages:chat_home'))  # Redirect to chat home page after signup
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        form = MyUserCreationForm()
    return render(request, 'user/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)  # Log in the user after authentication
            return redirect(reverse_lazy('my_messages:chat_home'))  # Redirect to chat home page after login
        else:
            return render(request, 'user/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'user/login.html')

def logout_view(request):
    logout(request)  # Log out the user
    return redirect('home')  # Redirect to home page after logout

def password_reset_request(request):
    if request.method == "POST":
        form = MyPasswordResetForm(request.POST)
        if form.is_valid():
            form.save()  # Send password reset email
            return redirect('password_reset_done')  # Redirect after successful form submission
    else:
        form = MyPasswordResetForm()
    return render(request, 'user/password_reset.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    if request.method == "POST":
        form = MySetPasswordForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new password
            return redirect('user:password_reset_complete')  # Redirect to password reset complete page
    else:
        form = MySetPasswordForm()
    return render(request, 'user/password_reset_confirm.html', {'form': form})
