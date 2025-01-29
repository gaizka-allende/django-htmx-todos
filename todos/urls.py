# todos/urls.py
from django.urls import path

from todos.views import index, login, logout_view, register, admin


urlpatterns = [
    path('', index),
    path('login', login),
    path('logout', logout_view),
    path('register', register),
    path('admin', admin)
]