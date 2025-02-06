# todos/views.py
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from todos.models import Todos, Suggestions
from todos.utils.date import formatTodoDate

@login_required(login_url='/login')
def index(request):
    todos = Todos.objects.filter(user=request.user)
    #todo add completed todos
    return render(request, 'index.html', {'todos': map(lambda todo: {
      'id': todo.id,
      'title': todo.title,
      'completed': todo.completed,
      'created_modified': formatTodoDate(todo.created_modified)
    }, todos)})

@login_required(login_url='/login')
def todo(request):
    #todo Forbidden (CSRF token missing.): /todo
    if request.method == 'POST':
      #print(request.POST.get('title'))
      return HttpResponse('Todo')

@login_required(login_url='/login')
def suggestions(request):
  title = request.GET.get('title')
  suggestions = Suggestions.objects.filter(title__icontains=title)
  print(suggestions[0].title)
  if suggestions is None:
    return HttpResponse('')
  else:
    #todo implement the highlighting of the title in the suggestion below in javascript
    #${suggestion.slice(0, suggestion.indexOf(title))}<span
    #  class="bg-yellow-300"
    #  >${title}</span
    #>${suggestion.slice(suggestion.indexOf(title) + title.length)}
    return render(request, 'suggestions.html', {'suggestions': suggestions})

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