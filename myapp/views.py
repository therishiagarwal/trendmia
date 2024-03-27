# myapp/views.py

from django.shortcuts import render, redirect, HttpResponse,render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db import transaction
from .forms import SignUpForm, UserLoginForm, ProjectForm
from datetime import datetime
from .models import CustomUser,Project
import os
import supabase

# Initialize Supabase client
supabase_url = 'https://oypasfbahsankiotfziv.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im95cGFzZmJhaHNhbmtpb3Rmeml2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTAwODIxNTEsImV4cCI6MjAyNTY1ODE1MX0.buYR2zFe7Y9mjNbDDvl--CVAWwb8XoQUN6y0iKKiyhg'
supabase_client = supabase.create_client(supabase_url, supabase_key)


def index(request):
    context = {
        "variable": "This is sent",
        "form": SignUpForm(),  # Pass the SignUpForm instance to the context
    }
    return render(request, 'index.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.signup_datetime = datetime.now()
                user.save()

                # Redirect to feed page upon successful signup
                return redirect('feed')
            except Exception as e:
                # Handle any exceptions
                print(e)
                # Redirect to homepage if an error occurs
                return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'index.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)  # Use Django's built-in AuthenticationForm
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Log the user in
                return redirect('feed')  # Redirect to the feed page upon successful login
            else:
                # Authentication failed, display an error message
                return render(request, 'login.html', {'login_form': form, 'error_message': 'Invalid username or password.'})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'login_form': form})

def logout_view(request):
    logout(request)
    return redirect('login')



def about(request):
    return HttpResponse("This is about page")


def contact(request):
    return HttpResponse("This is contact page")


def feed(request):
    # Your view logic here
    return render(request, 'feed.html')


@login_required
def post_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                project = form.save(commit=False)
                project.user = request.user
                project.created_at = datetime.now()  # Ensure 'created_at' is auto-generated in the model
                project.save()
                messages.success(request, 'Project posted successfully.')
                return HttpResponseRedirect('/feed')
            except Exception as e:
                messages.error(request, 'An error occurred while posting the project.')
                print(e)  # Print the exception for debugging
    else:
         messages.error(request, 'An error occurred while posting the project.')
         form = ProjectForm()
    return render(request, 'feed.html', {'form': form})