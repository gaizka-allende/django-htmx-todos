# todos/views.py
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from todos.models import Logins
from bcrypt import checkpw, hashpw, gensalt
from django.urls import reverse

def index(request):
  return render(request, 'index.html')

@csrf_exempt 
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = Logins.objects.filter(username=username).first()
        if user is None:
          return HttpResponse('User not found', status=404)
        if not checkpw(password.encode(), user.password.encode()):
          return HttpResponse('Password incorrect', status=401)
        request.session['username'] = username
        response = render(request, 'index.html')
        response['HX-Replace-Url'] = '/'
        return response
    elif request.method == 'GET':
      return render(request, 'login.html')
  
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
    if Logins.objects.filter(username=username).first() is not None:
      return HttpResponse('User already exists', status=400)
    Logins.objects.create(username=username, password=hashpw(password.encode(), gensalt()).decode())
    request.session['username'] = username
    return render(request, 'index.html')
  else:
    return render(request, 'register.html')


def admin(request):
    return HttpResponse('<h1>Admin</h1>')