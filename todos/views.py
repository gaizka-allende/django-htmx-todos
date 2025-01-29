# todos/views.py
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from todos.models import Logins
from bcrypt import checkpw

def index(request):
  html = f'''
  <html>
      <body>
          <h1>Todos</h1>
      </body>
  </html>
  '''
  return HttpResponse(html)

@csrf_exempt 
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = Logins.objects.filter(username=username).first()
        if user is None:
          return HttpResponse('User not found', status=404)
        if not checkpw(request.POST.get('password').encode(), user.password.encode()):
          return HttpResponse('Password incorrect', status=401)
        request.session['username'] = username
        return render(request, 'loggedIn.html', {username})
    elif request.method == 'GET':
      return render(request, 'login.html')
  
def logout_view(request):
    logout(request)
    return render(request, 'loggedOut.html')

def admin(request):
    return HttpResponse('<h1>Admin</h1>')