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



class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)  # Automatically set the date field

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Project(models.Model):
    TAG_CHOICES = (
        ('AI', 'AI'),
        ('Data Science', 'Data Science'),
        ('Web Development', 'Web Development'),
        ('Finance', 'Finance'),
        ('Iot', 'Iot'),
        ('App Development', 'App Development'),
        ('Health', 'Health'),
        ('Productivity', 'Productivity'),
        ('Entertainment', 'Entertainment'),
        ('E-commerce', 'E-commerce'),
        ('Education', 'Education'),
        ('Cloud', 'Cloud'),
        ('Sports', 'Sports'),
        ('Robotics', 'Robotics'),
        ('Drones', 'Drones'),
        ('Mechanical', 'Mechanical'),
        ('Cybersecurity', 'Cybersecurity'),
        ('Ar/Vr', 'Ar/Vr'),
        ('Blockchain', 'Blockchain'),
        ('Environmental Sustainability', 'Environmental Sustainability'),
        # Add other choices here
    )

    heading = models.TextField()
    project_name = models.TextField()
    project_description = models.TextField()
    tag = models.CharField(max_length=100, choices=TAG_CHOICES)
    status = models.CharField(max_length=20, choices=[('ongoing', 'Ongoing'), ('completed', 'Completed')])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name
