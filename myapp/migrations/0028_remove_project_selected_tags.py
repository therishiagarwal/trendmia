# Generated by Django 4.1.5 on 2024-04-10 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0027_project_selected_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='selected_tags',
        ),
    ]
