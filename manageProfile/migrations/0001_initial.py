# Generated by Django 4.1.3 on 2022-12-15 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Persons',
            fields=[
                ('personId', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('IdentityNumber', models.CharField(max_length=13, unique=True)),
                ('FirstName', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Athlete',
            fields=[
                ('AthleteID', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('ProfileImage', models.ImageField(upload_to='manageProfile/Images/')),
                ('Federation', models.TextField(max_length=50)),
                ('PlayerType', models.TextField(max_length=50)),
                ('AthleteLevel', models.CharField(max_length=50)),
                ('ClubName', models.TextField(max_length=50)),
                ('ClubLevel', models.CharField(max_length=50)),
                ('JoinDate', models.DateTimeField()),
                ('personId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manageProfile.persons')),
            ],
        ),
    ]