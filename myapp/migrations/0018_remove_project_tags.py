# Generated by Django 4.1.5 on 2024-04-09 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_project_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='tags',
        ),
    ]
