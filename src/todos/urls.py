# todos/urls.py
from django.urls import path

from todos.views import index, login_view, logout_view, register, admin, createTodo, suggestions, updateTodo, account

urlpatterns = [
    path('', index, name='index'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('register', register, name='register'),
    path('account', account, name='account'),
    path('admin', admin, name='admin'),
    path('todo', createTodo, name='createTodo'),
    path('todo/<int:id>', updateTodo, name='updateTodo'),
    path('suggestions', suggestions, name='suggestions'),
]