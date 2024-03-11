# views.py

# views.py

from django.shortcuts import render, redirect, HttpResponse
from .forms import SignUpForm, UserLoginForm
from django.contrib.auth.views import LoginView


def index(request): 
    context = {
        "variable": "This is sent",
        "form": SignUpForm(),  # Pass the SignUpForm instance to the context
        "login_form": UserLoginForm()

    }
    return render(request, 'index.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Process form data
            # For example, create a new user object and save it
            # user = User.objects.create_user(username=form.cleaned_data['username'], ...)
            # Redirect to a success page or homepage
            return redirect('home')
    # If the form is invalid or the request method is not POST,
    # render the index.html template with the form instance
    return render(request, 'index.html', {'form': SignUpForm()})


def about(request):
    return HttpResponse("This is aboutpage")

def contact(request):
    return HttpResponse("This is contact page")
login = LoginView.as_view(template_name='index.html', authentication_form=UserLoginForm)
