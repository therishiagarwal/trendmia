# myapp/model.py 

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)  # Set the date field to auto-generate the current date

    def __str__(self):
        return self.username

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='project_images/')  # Assuming you want to upload project images
    tags = models.CharField(max_length=100)  # You can adjust this field based on your requirements

    # You can add more fields as needed

    def __str__(self):
        return self.title