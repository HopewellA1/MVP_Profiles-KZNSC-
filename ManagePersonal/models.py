from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Persons(models.Model):
    personId = models.IntegerField(primary_key=True, blank=False,null=False,auto_created=True)
    IdentityNumber = models.CharField(db_column='IdentityNumber', max_length=13) 
    FirstName = models.CharField(db_column='FirstName', max_length=50)  
    Middlename = models.CharField(db_column='MiddleName', max_length=50)  
    lastname = models.CharField(db_column='Lastname', max_length=50) 
    altcellphone = models.CharField(db_column='AltCellPhone', max_length=20) 
    altemail = models.CharField(db_column='AltEmail', max_length=50) 
    physicaladdress1 = models.CharField(db_column='PhysicalAddress1', max_length=100) 
    physicaladdress2 = models.CharField(db_column='PhysicalAddress2', max_length=100)  
    shoesize = models.IntegerField(db_column='ShoeSize', blank=True, null=True)  
    tracksuitsize = models.IntegerField(db_column='TrackSuitSize', blank=True, null=True)
    disability = models.CharField(db_column='Disability', max_length=100)  
    disabilitydescription = models.CharField(db_column='DisabilityDescription', max_length=300) 
    gender = models.CharField(db_column='Gender', max_length=20)  
    ethnicity = models.CharField(db_column='Ethnicity', max_length=50)  
    cellphone = models.CharField(db_column='Cellphone', max_length=20)  
    NumProfile = models.IntegerField(default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    class Meta:
        
        db_table = 'Person'



class Nextofkin(models.Model):

    ID = models.IntegerField(primary_key=True,blank=False,null=False,auto_created=True) 
    Title = models.CharField(db_column='Title', max_length=100) 
    FirstName = models.CharField(db_column='FirstName', max_length=100)  
    Surname = models.CharField(db_column='Surname', max_length=100)  
    Relationship = models.CharField(db_column='Relationship', max_length=100) 
    Jobtitle = models.CharField(db_column='JobTitle', max_length=100)  
    JobDescription = models.CharField(db_column='JobDescription', max_length=100) 
    HomeAddress = models.CharField(db_column='HomeAddress', max_length=100)
    WorkAddress = models.CharField(db_column='WorkAddress', max_length=100)  
    EmailAddress = models.CharField(db_column='EmailAddress', max_length=100)  
    PhoneNumber = models.CharField(db_column='PhoneNumber', max_length=20)  
    Gender = models.CharField(db_column='Gender', max_length=20)
    personId = models.ForeignKey(Persons,on_delete=models.CASCADE)
    class Meta:
        
        db_table = 'NextOfKin'

 
    

class Education(models.Model):
    education_id = models.AutoField(db_column='Education_Id', primary_key=True) 
    EducationLevel = models.CharField(db_column='EducationLevel', max_length=50)  
    SchoolAddress = models.CharField(db_column='SchoolAddress', max_length=50)  
    
    YearStarted = models.DateField(db_column='YearStarted', blank=True, null=True)  
    YearEnd = models.DateField(db_column='YearEnd', blank=True, null=True)  
    Completed = models.BooleanField(db_column='Completed',default=False) 
    personId = models.ForeignKey(Persons,on_delete=models.CASCADE)  

    class Meta:
      
        db_table = 'Education'

class Employment(models.Model):
    Employment_id = models.AutoField(db_column='Employment_ID', primary_key=True)  
    CompanyName = models.CharField(db_column='CompanyName', max_length=100) 
    CompanyAddress = models.CharField(db_column='CompanyAddress', max_length=100)  
    CurrentlyWorking = models.BooleanField(db_column='CurrentlyWorking',default=False)  
    Telephone = models.CharField(db_column='Telephone', max_length=20) 
    WorkPosition = models.CharField(db_column='WorkPosition', max_length=100) 
    StartDate = models.DateField(db_column='StartDate', blank=True, null=True)  
    EndDate = models.DateField(db_column='EndDate', blank=True, null=True)  
    Skills = models.CharField(db_column='SKills', max_length=100) 
    personId = models.ForeignKey(Persons,on_delete=models.CASCADE)  

    class Meta:
        
        db_table = 'Employment'
        
        
        
class Doctorsinformation(models.Model):
    DoctorsId = models.AutoField(db_column='DoctorsId', primary_key=True) 
    FirstName = models.CharField(db_column='FirstName', max_length=50)  
    Surname = models.CharField(db_column='Surname', max_length=50) 
    Speciality = models.CharField(db_column='Speciality', max_length=50)  
    Role = models.CharField(db_column='Role', max_length=50) 
    CellNumber = models.IntegerField(db_column='CellNumber', blank=True, null=True)  
    EmailAddress = models.CharField(db_column='EmailAddress', max_length=50) 
    WorkAddress = models.CharField(db_column='WorkAddress', max_length=50) 
    WorkTel = models.IntegerField(db_column='WorkTel', blank=True, null=True)  
    personId = models.ForeignKey(Persons,on_delete=models.CASCADE)   

    class Meta:
       
        db_table = 'DoctorsInformation'