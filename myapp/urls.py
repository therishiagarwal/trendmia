# myapp/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from myapp import views
from myapp.forms import UserLoginForm


urlpatterns = [
    path("", views.index, name='home'),
    path("about/", views.about, name='about'),
    path("contact/", views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('feed/', views.feed, name='feed'),
    path('post_project/', views.post_project, name='post_project'),
    path('logout/', views.logout_view, name='logout'),
]