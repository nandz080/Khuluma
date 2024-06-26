from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm, MyPasswordResetForm, MySetPasswordForm


# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            #username = form.cleaned_data.get('username')
            #raw_password = form.cleaned_data.get('<PASSWORD>')
            #user = authenticate(username=username, password=<PASSWORD>)
            login(request, user)
            return redirect('home')
        else:
            form = MyUserCreationForm()
        return render(request,'signup.html', {'form': form})
    

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'user/login.html', {'error': 'Invalid username or password'})
        return render(request, 'user/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')

def password_reset_request(request):
    if request.method == "POST":
        form = MyPasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_reset_done')
        else:
            form = MyPasswordResetForm()
        return render(request, 'user/password_reset.html', {'form': form})
    
def password_reset_confirm(request, uidb64, token):
    if request.method == "POST":
        form = MySetPasswordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:password_reset_complete')
        else:
            form = MySetPasswordForm()
        return render(request, 'user/password_reset_confirm.html', {'form': form})
    
        
   
  