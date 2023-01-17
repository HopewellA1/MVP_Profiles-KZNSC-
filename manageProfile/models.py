import datetime
from django.db import models
from tkinter import CASCADE
from turtle import position
from django.db import models
from django.contrib.auth.models import User
from ManagePersonal.models import Persons





class Parent(models.Model):
    ParentId = models.AutoField(primary_key=True,blank=False,null=False,auto_created=True)
    ProfileImage = models.ImageField(upload_to='manageProfile/images',blank=True, null=True)
    personId = models.ForeignKey(Persons,on_delete=models.CASCADE)
    JoinDate = models.DateTimeField() 
    Default = models.BooleanField(default=False)
    Status = models.CharField(max_length=50, default='Active')
    class Meta:
        
        db_table = 'Parent'
class Athlete(models.Model):
    AthleteID = models.AutoField(primary_key=True,blank=False,null=False,auto_created=True)
    
    ProfileImage = models.ImageField(upload_to='manageProfile/images',blank=True, null=True)
    
    
 
    Federation = models.TextField(max_length=50)
    PlayerType = models.TextField(max_length=50)
    AthleteLevel = models.CharField(max_length=50)
    ClubName = models.TextField(max_length=50)
    ClubLevel = models.CharField(max_length=50)
    JoinDate = models.DateTimeField() 
    Default = models.BooleanField(default=False)
    Status = models.CharField(max_length=50, default='Active')
    personId = models.ForeignKey(Persons,blank=True,null=True,on_delete=models.CASCADE)
    ParentId = models.ForeignKey(Parent,blank=True,null=True,on_delete=models.CASCADE)
    class Meta:
        
        db_table = 'Athlete'
class Coach(models.Model):
    CoachID = models.AutoField(primary_key=True,blank=False,null=False,auto_created=True)
    ProfileImage = models.ImageField(upload_to='manageProfile/images',blank=True, null=True)
    
    personId = models.ForeignKey(Persons,on_delete=models.CASCADE)
    CoachLevel = models.CharField(max_length=50)
    Status = models.CharField(max_length=50, default='Active')
    Default = models.BooleanField(default=False)
    JoinDate = models.DateTimeField() 
    Federation = models.TextField(max_length=50)  
    ClubName = models.TextField(max_length=50)
    class Meta:
        
        db_table = 'Coach'

class Official(models.Model):
    OfficialID = models.AutoField(db_column='OfficialID', primary_key=True,blank=False,null=False,auto_created=True)
    #OfficialID = models.IntegerField(primary_key=True,blank=False,null=False,auto_created=True)
    personId = models.ForeignKey(Persons,on_delete=models.CASCADE)
    ProfileImage = models.ImageField(upload_to='manageProfile/images',blank=True, null=True)
    Position = models.TextField(max_length=50)
    JoinDate = models.DateTimeField() 
    Default = models.BooleanField(default=False)
    Status = models.CharField(max_length=50, default='Active')
    Federation = models.TextField(max_length=50)
    
    class Meta:
        
        db_table = 'Official'
    
    
    
class Achievement(models.Model):
    AchievementId = models.AutoField(db_column='AchievementId', primary_key=True)
    TypeOfAchievement = models.CharField(db_column='TypeOfAchievement', max_length=50)
    NameOfAchievement = models.CharField(db_column='NameOfAchievement', max_length=50)
    Organization = models.CharField(db_column='Organization', max_length=50)
    YearOfAchievement = models.DateField(db_column='YearOfAchievement', blank=True, null=True, default='<jamming-date>')
    Certificate = models.CharField(db_column='Certificate', max_length=50)
  
   # ExecutiveID = models.IntegerField(db_column='ExecutiveID', blank=True, null=True)
    #ExecutiveID = models.IntegerField(db_column='ExexutiveID', blank=True, null=True)
    OfficialID = models.ForeignKey(Official, on_delete=models.CASCADE ,blank=True, null=True)
    CoachID = models.ForeignKey(Coach, on_delete=models.CASCADE,blank=True, null=True)
    AthleteID = models.ForeignKey(Athlete, on_delete=models.CASCADE,blank=True, null=True)
    class Meta:
        db_table = 'Achievements'