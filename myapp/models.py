# myapp/models.py

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import migrations, models


def set_default_tag(apps, schema_editor):
    Project = apps.get_model('myapp', 'Project')
    default_tag = 'AI'  # Choose any existing tag choice
    Project.objects.filter(tag=None).update(tag=default_tag)

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', 'previous_migration_number'),  # Replace 'previous_migration_number' with the actual migration number
    ]

    operations = [
        migrations.RunPython(set_default_tag),
    ]


    

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Project(models.Model):
    heading = models.TextField()
    project_name = models.TextField()
    project_description = models.TextField()
    status = models.CharField(max_length=20, choices=[('ongoing', 'Ongoing'), ('completed', 'Completed')])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=255)  # Store comma-separated tags

    def __str__(self):
        return self.project_name


from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
# myapp/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUserManager(models.Manager):
    pass  # Add any custom methods or functionality here if needed

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)  # Add the name field
    date = models.DateField(auto_now_add=True)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

