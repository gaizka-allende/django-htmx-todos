# todos/views.py
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render


def index(request):

  
  now = datetime.now()
  html = f'''
  <html>
      <body>
          <h1>Todos</h1>
          <p>The current time is { now }.</p>
      </body>
  </html>
  '''
  return HttpResponse(html)

def t(key):
    return key

def login(request):
    
    if request.method == 'POST':
        print('set username')
        username = request.POST.get('username')
        request.session['username'] = username
        return HttpResponse(f'<h1>Logged in as {username}</h1>')
    elif request.method == 'GET':
      return render(request, 'login.html')
      return HttpResponse(
        f'''
      ''')
    
  
def logout(request):
    request.session.flush()
    response = HttpResponse('<h1>Logout</h1>')
    #response.delete_cookie('session')
    return response

def admin(request):
    return HttpResponse('<h1>Admin</h1>')