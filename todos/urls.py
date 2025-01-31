# todos/urls.py
from django.urls import path

from todos.views import index, login, logout_view, register, admin


urlpatterns = [
    path('', index, name='index'),
    path('login', login, name='login'),
    path('logout', logout_view, name='logout'),
    path('register', register, name='register'),
    path('admin', admin, name='admin'),
]