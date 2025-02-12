# todos/views.py
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from todos.models import Todos, Suggestions
import datetime
from django.http.request import QueryDict

#todo add translations

@login_required(login_url='/login')
def index(request):
    uncompletedTodos = Todos.objects.filter(user=request.user).order_by('-created_modified').filter(completed=0)
    completedTodos = Todos.objects.filter(user=request.user).order_by('-created_modified').filter(completed=1)  
    return render(request, 'index.html', {'uncompletedTodos': map(lambda todo: {
      'id': todo.id,
      'title': todo.title,
      'completed': todo.completed,
      'created_modified': datetime.datetime.fromisoformat(todo.created_modified)
    }, uncompletedTodos), 'completedTodos': map(lambda todo: {  
      'id': todo.id,
      'title': todo.title,
      'completed': todo.completed,
      'created_modified': datetime.datetime.fromisoformat(todo.created_modified)
    }, completedTodos), 'uncompletedTodosCount': len(uncompletedTodos)})

@login_required(login_url='/login')
def createTodo(request):
    if request.method == 'POST':
      title = request.POST.get('title')
      todo = Todos.objects.create(user=request.user, title=title, completed=0, created_modified=datetime.datetime.now())   
      if todo is None:
        return HttpResponse('Error creating todo', status=500)
      uncompletedTodos = Todos.objects.filter(user=request.user).order_by('-created_modified').filter(completed=0)
      uncompletedTodos = list(map(lambda todo: {
        'id': todo.id,
        'title': todo.title,
        'completed': todo.completed,
        'created_modified': datetime.datetime.fromisoformat(todo.created_modified)
      }, uncompletedTodos))
      completedTodos = Todos.objects.filter(user=request.user).order_by('-created_modified').filter(completed=1)  
      completedTodos = list(map(lambda todo: {  
        'id': todo.id,
        'title': todo.title,
        'completed': todo.completed,
        'created_modified': datetime.datetime.fromisoformat(todo.created_modified)
      }, completedTodos))
      return render(request, 'todos.html',{'uncompletedTodos': uncompletedTodos, 'completedTodos': completedTodos, 'uncompletedTodosCount': len(uncompletedTodos)})
                    
@login_required(login_url='/login')
def updateTodo(request, id):
  todo = Todos.objects.get(id=id)
  if request.method == 'DELETE':
    todo.delete()
  elif request.method == 'PATCH':
    formData = QueryDict(request.body)
    if formData.get('checkbox_' + str(id)) is not None:
      todo.completed = 1
    else:
      todo.completed = 0
    #this is not working
    todo.created_modified = datetime.datetime.now()
    todo.save()
  elif request.method == 'PUT':
    formData = QueryDict(request.body)
    title = formData.get('textbox_' + str(id))
    todo.title = title
    todo.created_modified = datetime.datetime.now()
    todo.save()
  uncompletedTodos = Todos.objects.filter(user=request.user).order_by('-created_modified').filter(completed=0)
  uncompletedTodos = list(map(lambda todo: {
      'id': todo.id,
      'title': todo.title,
      'completed': todo.completed,
      'created_modified': datetime.datetime.fromisoformat(todo.created_modified)
    }, uncompletedTodos))
  completedTodos = Todos.objects.filter(user=request.user).order_by('-created_modified').filter(completed=1)  
  completedTodos = list(map(lambda todo: {  
      'id': todo.id,
      'title': todo.title,
      'completed': todo.completed,
      'created_modified': datetime.datetime.fromisoformat(todo.created_modified)
    }, completedTodos))
  return render(request, 'todos.html', {'uncompletedTodos': uncompletedTodos, 'completedTodos': completedTodos, 'uncompletedTodosCount': len(uncompletedTodos)})
                
@login_required(login_url='/login')
def suggestions(request):
  title = request.GET.get('title')
  suggestions = Suggestions.objects.filter(title__icontains=title)
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