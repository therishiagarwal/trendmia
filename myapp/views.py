# myapp/views.py

from django.shortcuts import render, redirect, HttpResponse,render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from .forms import SignUpForm, ProjectForm
from datetime import datetime
import supabase
from .models import Tag,Project
from django.utils import timezone
import pytz

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

# def trending(request):
#     return HttpResponse("This is t page")

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

from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ipywidgets as widgets

def trending(request):
    # Load and process data
    data = pd.read_excel('projects.xlsx', sheet_name='Sheet1')
    data['date/timestamp'] = pd.to_datetime(data['date/timestamp'])
    data['month_year'] = data['date/timestamp'].dt.to_period('M')
    data['tags'] = data['tags'].str.split(', ')

    # Calculate tag counts
    unique_months = sorted(data['month_year'].unique())
    weights = {month: 1 / (len(unique_months) - i) for i, month in enumerate(unique_months)}
    tag_counts = {}
    for index, row in data.iterrows():
        for tag in row['tags']:
            tag_counts[tag] = tag_counts.get(tag, 0) + weights[row['month_year']]

    # Sort tag counts
    tag_counts_sorted = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)

    # Dropdown widget for tag selection
    tag_dropdown = widgets.Dropdown(
        options=list(tag_counts.keys()),
        description='Select Tag:',
        disabled=False
    )

    context = {
        'tag_counts': tag_counts_sorted,
        'tag_dropdown': tag_dropdown
    }

    return render(request, 'trending.html', context)

def contact(request):
    return HttpResponse("This is contact page")



def feed(request):
    # Retrieve all projects from the database
    posts = Project.objects.all().order_by('-created_at')
    # Retrieve all tags from the database
    tags = Tag.objects.all()
    # Pass the projects and tags to the template context
    return render(request, 'feed.html', {'posts': posts, 'tags': tags})


@login_required
def post_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)  # Debugging: Print form data
            try:
                project = form.save(commit=False)
                project.user = request.user
                project.created_at = datetime.now()  
                project.save()  # Save project data to the database
                print("Project saved successfully")  # Debugging: Print success message
                # Redirect to the feed page upon successful submission
                return redirect('feed')
            except Exception as e:
                # Handle errors
                print("Error saving project:", e)  # Debugging: Print error message
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            # Form is invalid, return error response
            print("Form errors:", form.errors)  # Debugging: Print form errors
            return JsonResponse({'success': False, 'error': 'Invalid form data'})
    else:
        # Method is not POST, return error response
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
from django.shortcuts import render

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ChatMessage
from .models import ChatMessage, CustomUser, Project  # Import the Project model
from .models import ChatMessage, CustomUser, Project  # Import the Project model

@login_required
def chat_page(request, username):
    try:
        recipient = CustomUser.objects.get(username=username)
        if request.method == 'POST':
            message = request.POST.get('message')
            project_id = request.POST.get('project_id')  # Assuming you pass the project_id in the request
            project = Project.objects.get(id=project_id)  # Retrieve the project object
            if message and project:  # Check if both message and project are provided
                ChatMessage.objects.create(sender=request.user, recipient=recipient, project=project, message=message)
                # Redirect to the same chat page after sending the message
                return redirect('chat_page', username=username)
            else:
                # Handle empty message or missing project
                return HttpResponse("Message cannot be empty and Project must be provided")
        else:
            messages = ChatMessage.objects.filter(sender=request.user, recipient=recipient) | \
                       ChatMessage.objects.filter(sender=recipient, recipient=request.user)
            return render(request, 'chat.html', {'messages': messages, 'recipient': recipient})
    except CustomUser.DoesNotExist:
        return HttpResponse("User not found")


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatMessage, Project

@login_required
def some_view_function(request):
    if request.method == 'POST':
        recipient_username = request.POST.get('recipient_username')
        message = request.POST.get('message')
        project_name = request.POST.get('project_name')
        project_description = request.POST.get('project_description')
        # Assuming you also have the recipient user object based on the recipient username
        
        # Assuming project_data is populated based on the form data
        project_data = {
            'name': project_name,
            'description': project_description,
            'owner': request.user,
            'created_at': datetime.now(),
            # Add other project attributes as needed
        }

        # Get or create a Project object
        project, _ = Project.objects.get_or_create(**project_data)

        if recipient_username and message:
            try:
                recipient = CustomUser.objects.get(username=recipient_username)
                # Create a new ChatMessage object
                chat_message = ChatMessage.objects.create(
                    sender=request.user,
                    recipient=recipient,
                    project=project,
                    message=message
                )
                return redirect('chat_page', username=recipient_username)
            except CustomUser.DoesNotExist:
                return HttpResponse("Recipient not found")
        else:
            return HttpResponse("Recipient username and message are required")
    else:
        return HttpResponse("Invalid request method")

