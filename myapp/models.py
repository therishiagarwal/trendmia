# myapp/model.py 

from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.db import models

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)  # Set the date field to auto-generate the current date

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
class Project(models.Model):
    heading = models.CharField(max_length=100)
    project_name = models.CharField(max_length=100)
    project_description = models.TextField()
    category = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[('ongoing', 'Ongoing'), ('completed', 'Completed')])
    media = models.FileField(upload_to='media/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.project_name