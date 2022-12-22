import datetime
from django.db import models
from tkinter import CASCADE
from turtle import position
from django.db import models
from django.contrib.auth.models import User


class Persons(models.Model):
    personId = models.IntegerField(primary_key=True, blank=False,null=False,auto_created=True)
    IdentityNumber = models.CharField(null=False, max_length=13,unique=True)
    FirstName = models.TextField()
    NumProfile= models.IntegerField(default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)


class Parent(models.Model):
    ParentId = models.IntegerField(primary_key=True,blank=False,null=False,auto_created=True)
    ProfileImage = models.ImageField(upload_to='manageProfile/images',blank=True, null=True)
    personId = models.ForeignKey(Persons,on_delete=models.CASCADE)
    JoinDate = models.DateTimeField() 
    Default = models.BooleanField(default=False)
    Status = models.CharField(max_length=50, default='Active')
    
class Athlete(models.Model):
    
    ProfileImage = models.ImageField(upload_to='manageProfile/images',blank=True, null=True)
    AthleteID = models.IntegerField(primary_key=True,blank=False,null=False,auto_created=True)
 
    Federation = models.TextField(max_length=50)
    PlayerType = models.TextField(max_length=50)
    AthleteLevel = models.CharField(max_length=50)
    ClubName = models.TextField(max_length=50)
    ClubLevel = models.CharField(max_length=50)
    JoinDate = models.DateTimeField() 
    Default = models.BooleanField(default=False)
    Status = models.CharField(max_length=50, default='Active')
    personId = models.ForeignKey(Persons,on_delete=models.CASCADE)
    ParentId = models.ForeignKey(Parent,blank=True,null=True,on_delete=models.CASCADE)
