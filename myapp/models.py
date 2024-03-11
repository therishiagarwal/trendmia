# myapp/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import HttpResponse

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.username

# myapp/views.py
from django.shortcuts import render, redirect
from .forms import SignUpForm

def index(request): 
    context = {
        "variable": "This is sent",
        "form": SignUpForm()  # Pass the SignUpForm instance to the context
    }
    return render(request, 'index.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or homepage
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'index.html', {'form': form})

def about(request):
    return HttpResponse("This is about page")

def contact(request):
    return HttpResponse("This is contact page")
