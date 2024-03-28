# myapp/model.py 

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)  # Automatically set the date field

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Project(models.Model):
    heading = models.TextField()
    project_name = models.TextField()
    project_description = models.TextField()
    category = models.TextField()
    status = models.CharField(max_length=20, choices=[('ongoing', 'Ongoing'), ('completed', 'Completed')])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Set the creation date automatically

    def __str__(self):
        return self.project_name
