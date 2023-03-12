from django.urls import path
from rest_framework_casdoor import views


app_name = 'rest_framework_casdoor'
urlpatterns = [
    path('login', views.login, name='login'),
    path('callback', views.callback, name='callback')
]
