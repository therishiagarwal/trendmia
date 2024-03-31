# myapp/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from myapp.models import CustomUser
from .models import Project,Tag

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Enter Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())


class ProjectForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Project
        fields = ['heading', 'project_name', 'project_description', 'tags', 'status']
