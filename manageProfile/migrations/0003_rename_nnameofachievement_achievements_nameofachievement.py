# Generated by Django 4.1.3 on 2023-01-17 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manageProfile', '0002_achievements'),
    ]

    operations = [
        migrations.RenameField(
            model_name='achievements',
            old_name='nNameOfAchievement',
            new_name='NameOfAchievement',
        ),
    ]
