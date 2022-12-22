# Generated by Django 4.1.3 on 2022-12-21 19:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Persons',
            fields=[
                ('personId', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('IdentityNumber', models.CharField(max_length=13, unique=True)),
                ('FirstName', models.TextField()),
                ('NumProfile', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('ParentId', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('ProfileImage', models.ImageField(blank=True, null=True, upload_to='manageProfile/images')),
                ('JoinDate', models.DateTimeField()),
                ('Default', models.BooleanField(default=False)),
                ('Status', models.CharField(default='Active', max_length=50)),
                ('personId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manageProfile.persons')),
            ],
        ),
        migrations.CreateModel(
            name='Athlete',
            fields=[
                ('AthleteID', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('ProfileImage', models.ImageField(blank=True, null=True, upload_to='manageProfile/images')),
                ('Federation', models.TextField(max_length=50)),
                ('PlayerType', models.TextField(max_length=50)),
                ('AthleteLevel', models.CharField(max_length=50)),
                ('ClubName', models.TextField(max_length=50)),
                ('ClubLevel', models.CharField(max_length=50)),
                ('JoinDate', models.DateTimeField()),
                ('Default', models.BooleanField(default=False)),
                ('Status', models.CharField(default='Active', max_length=50)),
                ('ParentId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manageProfile.parent')),
                ('personId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manageProfile.persons')),
            ],
        ),
    ]
