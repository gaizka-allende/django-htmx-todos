# todos/urls.py
from django.urls import path

from todos.views import index, login, logout_view, admin


urlpatterns = [
    path('', index),
    path('login', login),
    path('logout', logout_view),
    path('admin', admin)
]