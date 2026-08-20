# accounts/views.py

''' 
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("core:home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    
    form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to the 'next' page if it exists, otherwise to home
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
            
    form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})
    
    '''
    
from django.shortcuts import render, redirect
from django.contrib import messages
import requests

def jwt_login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            response = requests.post('http://localhost:8000/api/token/', json={
                'username': username,
                'password': password
            })
        except requests.exceptions.RequestException:
            messages.error(request, "Auth service unavailable.")
            return render(request, 'accounts/jwt_login.html')

        if response.status_code == 200:
            tokens = response.json()
            request.session['access'] = tokens.get('access')
            request.session['refresh'] = tokens.get('refresh')
            messages.success(request, "Login successful with JWT.")
            return redirect("core:dashboard")
        else:
            messages.error(request, "Invalid credentials.")
    
    return render(request, 'accounts/jwt_login.html')
