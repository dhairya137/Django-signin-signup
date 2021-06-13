from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages, auth


def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      messages.success(request, "You are logged in")
      return redirect('dashboard')
    else:
      messages.error(request, "Invalid credentials")
      return redirect('login')

  return render(request, 'login.html')

def register(request):
  if request.method == 'POST':
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

    if password == confirm_password:
      if User.objects.filter(username=username).exists():
        messages.error(request, "Username already exists")
        return redirect('register')
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request, "Email already exists")
          return redirect('register')
        else:
          user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, email=email, password=password)
          user.save()
          messages.success(request, 'User created hurrey!!')
          return redirect('login')
    else:
      messages.error(request, 'Password does not match')
      return redirect('register')
  
  return render(request, 'register.html')

def logout_user(request):
  logout(request)
  return redirect('login')

@login_required(login_url='login')
def dashboard(request):
  return render(request, 'dashboard.html')