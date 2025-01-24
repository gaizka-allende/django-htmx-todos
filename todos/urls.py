# todos/urls.py
from django.urls import path

from todos.views import index, login, logout, admin


urlpatterns = [
    path('', index),
    path('login', login),
    path('logout', logout),
    path('admin', admin)
]