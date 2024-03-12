# urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from myapp import views

urlpatterns = [
    path("", views.index, name='home'),
    path("about/", views.about, name='about'),
    path("contact/", views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('feed/', views.feed, name='feed'),

]