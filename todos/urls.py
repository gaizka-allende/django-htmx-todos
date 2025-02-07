# todos/urls.py
from django.urls import path

from todos.views import index, login_view, logout_view, register, admin, todo, suggestions, deleteTodo


urlpatterns = [
    path('', index, name='index'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('register', register, name='register'),
    path('admin', admin, name='admin'),
    path('todo', todo, name='todo'),
    path('todo/<int:id>', deleteTodo, name='deleteTodo'),
    path('suggestions', suggestions, name='suggestions')
]