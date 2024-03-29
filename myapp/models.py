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
    CATEGORY_CHOICES = (
        ('AI', 'AI'),
        ('Data Science', 'Data Science'),
        ('Web Development', 'Web Development'),
        # Add other choices here
    )

    heading = models.TextField()
    project_name = models.TextField()
    project_description = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=[('ongoing', 'Ongoing'), ('completed', 'Completed')])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name
