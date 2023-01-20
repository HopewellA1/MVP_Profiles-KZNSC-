from unittest.util import _MAX_LENGTH
from django.db import models
from email.mime import image
from tkinter import CASCADE
from turtle import position
from django.db import models
from django.contrib.auth.models import User

class Register(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False)
    firstName = models.TextField()
    lastName=models.TextField()    
    gender= models.TextField()  #inlineRadioOptions
    dateOfBirth = models.DateField()
    phoneNumber = models.TextField()
    email = models.TextField()
    
    