# todos/views.py
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def index(request):
  return render(request, 'index.html')

@csrf_exempt 
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
          return HttpResponse('Invalid username or password', status=404)
        login(request, user)
        response = render(request, 'index.html')
        response['HX-Replace-Url'] = '/'
        return response
    elif request.method == 'GET':
      return render(request, 'login.html')
  
@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return render(request, 'loggedOut.html')

@csrf_exempt 
def register(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    reEnterPassword = request.POST.get('reEnterPassword')
    if password != reEnterPassword:
      return HttpResponse('Passwords do not match', status=400)
    if User.objects.filter(username=username).exists():
      return HttpResponse('User already exists', status=400)
    user = User.objects.create_user(username=username, password=password)
    if user is None:
      return HttpResponse('Error creating user', status=500)
    login(request, user)
    response = render(request, 'index.html')
    response['HX-Replace-Url'] = '/'
    return response
  else:
    return render(request, 'register.html')


@login_required(login_url='/login')
def admin(request):
    return HttpResponse('<h1>Admin</h1>')