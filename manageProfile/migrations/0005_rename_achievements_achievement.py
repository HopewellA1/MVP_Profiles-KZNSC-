# Generated by Django 4.1.3 on 2023-01-17 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manageProfile', '0004_remove_achievements_executiveid'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Achievements',
            new_name='Achievement',
        ),
    ]
