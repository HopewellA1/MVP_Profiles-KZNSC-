import datetime
from django.db import models
from tkinter import CASCADE
from turtle import position
from django.db import models


class Persons(models.Model):
    personId = models.IntegerField(primary_key=True, blank=False,null=False,auto_created=True)
    IdentityNumber = models.CharField(null=False, max_length=13,unique=True)
    FirstName = models.TextField()
    NumProfile= models.IntegerField(default=0)

class Athlete(models.Model):
    
    ProfileImage = models.ImageField(upload_to='manageProfile/images',blank=True, null=True)
    AthleteID = models.IntegerField(primary_key=True,blank=False,null=False,auto_created=True)
    personId = models.ForeignKey(Persons,on_delete=models.CASCADE)
    Federation = models.TextField(max_length=50)
    PlayerType = models.TextField(max_length=50)
    AthleteLevel = models.CharField(max_length=50)
    ClubName = models.TextField(max_length=50)
    ClubLevel = models.CharField(max_length=50)
    JoinDate = models.DateTimeField() 
    Default = models.BooleanField(default=False)
    Status = models.CharField(max_length=50, default='Active')