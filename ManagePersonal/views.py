from django.shortcuts import render
import json
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from manageProfile.models import Athlete,Parent,Coach,Official
from django.utils.dateparse import parse_date
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from ManagePersonal.models import Persons,Nextofkin,Education,Employment,Doctorsinformation,CustomField
from manageProfile import views 
from ManagePersonal.validate import calcControlDigit,validateID,getLastDigit
from Login.models import Register
# Create your views here.



def checkParent(Person):
    parent = False
    
    try:
        p = get_object_or_404(Parent, personId = Person)
        if p:
            parent = True  
        else:
            parent = False   
    except:
       parent = False 
    
    return parent




@login_required
def personal(request, id):
    #request.session['process'] = None
  
    user = request.user
    isParent = False
    register = get_object_or_404(Register, user=user)
    if request.method == 'GET':
        try:
            person = get_object_or_404(Persons, user = user) 
            
            p = Persons.objects.get(IdentityNumber = person.IdentityNumber)
            if person:
            
                if id != "0":
                    
                    messages.success(request,f"Dear {person.FirstName} please add your athlate personal information")
                    return render(request,'ManagePersonal/addPersonalInfo.html', {"parent": id,"register":register})
                    
                isParent =  checkParent(p)
                return render(request, 'manageProfile/ChooseProfile.html',{"person":person.personId, "isParent":isParent})
                
                   
            else:
                print("\n\ndid!\n\n") 
                
                      
        except:
            return render(request,'ManagePersonal/addPersonalInfo.html', {"parent": id,"register":register})
            
        
    if request.method == 'POST':
        
        
       
        if id != "0":
            if validateID(request.POST['IdentityNumber']) ==True and calcControlDigit(request.POST['IdentityNumber']) == getLastDigit(request.POST['IdentityNumber']):
                
                Person = Persons.objects.create(
                
                    IdentityNumber = request.POST['IdentityNumber'],
                    ethnicity= request.POST["ethnicity"],
                    FirstName = request.POST['FirstName'],
                    
                    Middlename = request.POST["Middlename"],
                    lastname = request.POST["lastname"],
                    altcellphone = request.POST["altcellphone"],
                    altemail = request.POST["altemail"],
                    physicaladdress1 = request.POST["physicaladdress1"],
                    physicaladdress2 = request.POST["physicaladdress2"],
                    shoesize = request.POST["shoesize"],
                    tracksuitsize = request.POST["tracksuitsize"],
                    disability = request.POST["disability"],
                    disabilitydescription = request.POST["disabilitydescription"],
                    gender = request.POST["gender"],
                    cellphone = request.POST["cellphone"],
                
                )
            else:
                messages.error(request,"Id number is not valid please correct and try again")
                return render(request,'ManagePersonal/addPersonalInfo.html', {"parent": id})
                
            p = Persons.objects.get(IdentityNumber = Person.IdentityNumber)
            ParentPerson = get_object_or_404(Persons, pk = id)
            
            #parent = get_object_or_404(Parent, personId = Person)
            messages.success(request,f"Dear { ParentPerson.FirstName}, Athlate personal information saved successfully please continue adding the required information below")
            
            request.session['process'] = "Parent"
            return redirect('addNextOfKin', PersonId = p.personId)
            return redirect('creatProfile', id=p.personId, profile="Parent",parent=ParentPerson.personId)
       
        else:
          
            if validateID(request.POST['IdentityNumber']) ==True and calcControlDigit(request.POST['IdentityNumber']) == getLastDigit(request.POST['IdentityNumber']):
                Person = Persons.objects.create(
                    IdentityNumber = request.POST['IdentityNumber'],
                    ethnicity= request.POST["ethnicity"],
                    FirstName = request.POST['FirstName'],
                    user = user,
                    Middlename = request.POST["Middlename"],
                    lastname = request.POST["lastname"],
                    altcellphone = request.POST["altcellphone"],
                    altemail = request.POST["altemail"],
                    physicaladdress1 = request.POST["physicaladdress1"],
                    physicaladdress2 = request.POST["physicaladdress2"],
                    shoesize = request.POST["shoesize"],
                    tracksuitsize = request.POST["tracksuitsize"],
                    disability = request.POST["disability"],
                    disabilitydescription = request.POST["disabilitydescription"],
                    gender = request.POST["gender"],
                    cellphone = request.POST["cellphone"],
                    
                    
                    
                )
            else:
                messages.error(request,"Id number is not valid please correct and try again")
                return render(request,'ManagePersonal/addPersonalInfo.html', {"parent": id})
               
            
            p = Persons.objects.get(IdentityNumber = Person.IdentityNumber)
            if request.POST["email"]:
                user.email = request.POST["email"]
                user.save()
            return redirect('addNextOfKin', PersonId = p.personId)
            #return render(request, 'manageProfile/ChooseProfile.html',{"person": p.personId})



#Updating the personal infomation
def updatePersonal(request, personId):
    user = request.user
    try:
        Person = get_object_or_404(Persons, pk = personId)
    except:
        pass
    
    if request.method =='GET':
         
        return render(request, 'ManagePersonal/updatePersonal.html',{"person": Person})
     
    if request.method =='POST':
        numUpdates = 0
        person = get_object_or_404(Persons, personId = personId)
        print(person)
        if request.POST["IdentityNumber"]:
            person.IdentityNumber = request.POST["IdentityNumber"]
            numUpdates += 1
            
        if request.POST["FirstName"]:
            person.FirstName = request.POST["FirstName"]
            numUpdates += 1
            
            
        if request.POST["Middlename"]:
            person.Middlename = request.POST["Middlename"]
            numUpdates += 1
                 
        if request.POST["lastname"]:
            person.lastname = request.POST["lastname"]
            numUpdates += 1
            
        if request.POST["gender"] == "select":
           pass
        else:
            person.gender = request.POST["gender"]
            numUpdates += 1
        
        if request.POST["ethnicity"] == "select":
           pass
        else:
            person.ethnicity = request.POST["ethnicity"]
            numUpdates += 1
        
        if request.POST["disability"] == "select":
           pass
        else:
            person.disability = request.POST["disability"]
            numUpdates += 1
        
        if request.POST["disabilitydescription"]:
            person.disabilitydescription = request.POST["disabilitydescription"]
            numUpdates += 1
        
        if request.POST["email"]:
            person.user.email = request.POST["email"]
            person.user.save()
            numUpdates += 1
            
        if request.POST["altemail"]:
            person.altemail = request.POST["altemail"]
            numUpdates += 1
            
        if request.POST["cellphone"]:
            person.cellphone = request.POST["cellphone"]
            numUpdates += 1
            
        if request.POST["altcellphone"]:
            person.altcellphone = request.POST["altcellphone"]
            numUpdates += 1
        
             
        if request.POST["tracksuitsize"]:
            person.tracksuitsize = request.POST["tracksuitsize"]
            numUpdates += 1
            
        if request.POST["shoesize"]:
            person.shoesize = request.POST["shoesize"]
            numUpdates += 1
        
        if request.POST["physicaladdress1"]:
            person.physicaladdress1 = request.POST["physicaladdress1"]
            numUpdates += 1
        
        if request.POST["physicaladdress2"]:
            person.physicaladdress1 = request.POST["physicaladdress2"]
            numUpdates += 1
        
        if numUpdates >0:
     
           
            person.save()
            messages.success(request,f"Dear you have successfully updated your personal infomation")
        else:
            messages.success(request,f"Dear {person.FirstName} you did not make any changes on you personal information")
            
        print(f"number of updates made: {numUpdates}")
        return redirect('updatePersonal', personId = Person.personId)





#Adding the next of kin information

@login_required
def addNextOfKin(request, PersonId):
    person = get_object_or_404(Persons, pk= PersonId)
    
    if request.method =='GET':
        
        messages.success(request,f"You must have atleast one next of kin information added")
        return render(request, 'ManagePersonal/addNextOfKin.html', {"person": person})
    
    if request.method == 'POST':
        nextofkin= Nextofkin.objects.create(
        personId = person,
        Title = request.POST["Title"],
        FirstName = request.POST["FirstName"],
        Surname = request.POST["Surname"],
        Relationship = request.POST["Relationship"],
        Jobtitle = request.POST["Jobtitle"],
        JobDescription = request.POST["JobDescription"],
        HomeAddress = request.POST["HomeAddress"],
        WorkAddress = request.POST["WorkAddress"],
        EmailAddress = request.POST["EmailAddress"],
        PhoneNumber = request.POST["PhoneNumber"],
        Gender = request.POST["Gender"],
        )
        
        messages.warning(request,"please double check these details, correct and/or continue.")
        kin = get_object_or_404(Nextofkin, personId = person)
        return redirect('updateNextOfKin', kinId = kin.ID, place="OnCreate")      
    

@login_required
def updateNextOfKin(request, kinId, place):
    
    nextofkin = get_object_or_404(Nextofkin, pk = kinId)
    kinPerson = nextofkin.personId
    
    if request.method =='GET':
        
        return render(request, 'ManagePersonal/updateNextOfKin.html', {"nextofkin":nextofkin,"person":kinPerson,"place":place})
    
    if request.method =='POST':
        
        
        numUpdates = 0
        if request.POST["Title"]:
            nextofkin.Title = request.POST["Title"]
            numUpdates +=1
            
        if request.POST["FirstName"]:
            nextofkin.FirstName = request.POST["FirstName"]
            numUpdates +=1
            
        if request.POST["Surname"]:
            nextofkin.Surname = request.POST["Surname"]
            numUpdates +=1
        
        if request.POST["Surname"]:
            nextofkin.Surname = request.POST["Surname"]
            numUpdates +=1
        
        if request.POST["Relationship"]:
            nextofkin.Relationship = request.POST["Relationship"]
            numUpdates +=1
        
        if request.POST["Jobtitle"]:
            nextofkin.Jobtitle = request.POST["Jobtitle"]
            numUpdates +=1
        
        if request.POST["JobDescription"]:
            nextofkin.JobDescription = request.POST["JobDescription"]
            numUpdates +=1
        
        if request.POST["HomeAddress"]:
            nextofkin.HomeAddress = request.POST["HomeAddress"]
            numUpdates +=1
            
        if request.POST["WorkAddress"]:
            nextofkin.WorkAddress = request.POST["WorkAddress"]
            numUpdates +=1
            
        if request.POST["EmailAddress"]:
            nextofkin.EmailAddress = request.POST["EmailAddress"]
            numUpdates +=1
            
        if request.POST["PhoneNumber"]:
            nextofkin.PhoneNumber = request.POST["PhoneNumber"]
            numUpdates +=1
            
        if request.POST["Gender"] == "select":
            pass
        else:
            nextofkin.Gender = request.POST["Gender"]
            numUpdates +=1
            
        if numUpdates > 0:
            
            nextofkin.save()
            messages.success(request,f"You have updated the next of kin information successfully")
        else:
            messages.success(request,f"You did not make any change on the information")
        if place =="OnCreate":   
            return redirect('updateNextOfKin', kinId = nextofkin.ID, place=place)
        if place =="OnView":
            return redirect('viewPerson', default = "NextOfKin", AtheId =0 )
        
        
#Adding the Education information
@login_required
def AddEducation(request, personId):
    
    person = get_object_or_404(Persons, pk = personId)
    
    if request.method =='GET':
        educations =getEducation(person)
        OnCreate = False
        
        if len(views.getProfiles(personId,"none")) == 0:
            OnCreate = True
        
        return render(request, 'ManagePersonal/AddEducation.html',{"person":person,"educations":educations,"OnCreate":OnCreate})
    
    if request.method == 'POST':
         
        completed = False
        try:
            if request.POST["Completed"] == 'on':
                completed = True
            
        except:
            pass
        
        education = Education.objects.create(
           
            HighestGrade = request.POST["HighestGrade"],
            InstitutionName = request.POST["InstitutionName"],
            EducationLevel = request.POST["EducationLevel"],
            SchoolAddress = request.POST["SchoolAddress"],
            YearStarted = request.POST["YearStarted"],
            YearEnd = request.POST["YearEnd"],
            Completed = completed,
            personId = person
            
        )
        
        messages.success(request,"Education information saved successfully")
        
        return redirect('AddEducation',personId=education.personId.personId)




#getting the education objects that belong to the person passed on the args
def getEducation(personObj):
    educations = [] 
    try:
        eds = Education.objects.all()
        for item in eds:
            if item.personId == personObj:
                educations.append(item)
    except:
        pass
    
    return educations


#Updating education information 
@login_required
def updateEducation(request, educationId, place):
    education = get_object_or_404(Education, pk = educationId)
    
    if request.method == 'GET':
        
        
        
        return render(request,'ManagePersonal/updateEducation.html',{"education":education,"place":place,"person":education.personId})
    
    
    if request.method =='POST':
        numUpdates = 0
        completed = False
        if request.POST["InstitutionName"]:
            education.InstitutionName = request.POST["InstitutionName"]
            numUpdates +=1
        if request.POST["HighestGrade"]:
            education.HighestGrade = request.POST["HighestGrade"]
            numUpdates +=1
        if request.POST["EducationLevel"]:
            education.EducationLevel = request.POST["EducationLevel"]
            numUpdates +=1
            
        if request.POST["SchoolAddress"]:
            education.SchoolAddress = request.POST["SchoolAddress"]
            numUpdates +=1
        
        if request.POST["YearStarted"]:
            education.YearStarted = request.POST["YearStarted"]
            numUpdates +=1
        
        if request.POST["YearEnd"]:
            education.YearEnd = request.POST["YearEnd"]
            numUpdates +=1
        try:
                
            if request.POST["Completed"] =='on':
                completed = True
                education.Completed = completed
                numUpdates +=1
            if request.POST["Completed"] == 'OldOn':
                pass
        except:
            if education.Completed == True:
                education.Completed = False
                numUpdates +=1
            pass
        if numUpdates > 0:
            education.save()
            messages.success(request, 'You have successfully updated the ducation information')
        else:
            messages.error(request,'You did not make any changes on the record')
           
        return redirect('updateEducation',educationId = education.education_id,place=place)
    
    
#getting all the education achievements belonging to the specified person
# def getEducation(personID):
    
#     person = get_object_or_404(Persons, pk = personID)
#     educations =[]
#     ads = Education.objects.all()
    
#     for item in ads:
#         if item.personId == person:
#             educations.append(item)
            
#     return educations   
    
    
    
#removing education information
@login_required
def removEducation(request, educationId, place):
    education = get_object_or_404(Education, pk = educationId)
    person = education.personId
    
    if request.method == 'GET':
        messages.error(request,"Are you sur you want to remove this record?")
        
        return render(request, 'ManagePersonal/removEducation.html',{"education":education,"place":place,"Person":person})
    
    if request.method =='POST':
        education.delete()
        
        messages.success(request,f"You have successfully removed the education in formation")
        if place == "OnCreate":
            return redirect('AddEducation',personId = person.personId)
        if place == "OnView":
            return redirect('viewPerson',default = "Education", AtheId=0 )
            
        
        
#creating the employment objects for the currently rejistering 

    
@login_required
def addEmployment(request, personId):
    
    person = get_object_or_404(Persons,pk=personId)
    
    if request.method == 'GET':
        employments = getEmployment(personId=person.personId)
        OnCreate = False
        
        if len(views.getProfiles(personId,"none")) == 0:
            OnCreate = True
        return render(request, 'ManagePersonal/addEmployment.html', {"person":person, "employments": employments, "OnCreate": OnCreate})
    
    if request.method == 'POST':
        currentlyWorking = False
        try:
            if request.POST["CurrentlyWorking"] == 'on':
                currentlyWorking = True
        except:
            currentlyWorking = False
        employment = Employment.objects.create(
            CompanyName = request.POST["CompanyName"],
            CompanyAddress = request.POST["CompanyAddress"],
            CurrentlyWorking = currentlyWorking,
            Telephone = request.POST["Telephone"],
            WorkPosition = request.POST["WorkPosition"],
            StartDate = request.POST["StartDate"],
            EndDate = request.POST["EndDate"],
            Skills = request.POST["Skills"],
            personId = person
        )
        
        messages.success(request, f"You have successfully added you emploment information, add more or proceed")
        return redirect('addEmployment', personId =employment.personId.personId )
    
    
    
    
    
def getEmployment(personId):
    person = get_object_or_404(Persons, pk=personId)
    employments =[]
    
    emple = Employment.objects.all()
    for item in emple:
        if item.personId == person:
            employments.append(item)
    
    return employments

#updating Employment information
@login_required
def updateEmployment(request, employmentId,place):
    
    employment = get_object_or_404(Employment, pk=employmentId)
    person = employment.personId
    
    if request.method == 'GET':
        
        return render(request, 'ManagePersonal/updateEmployment.html', {"employment":employment,"person":person,"place":place,"Person":person})
    
    if request.method == 'POST':
        numUpdates = 0
        if request.POST["CompanyName"]:
           employment.CompanyName = request.POST["CompanyName"]
           numUpdates += 1
        
        if request.POST["CompanyAddress"]:
           employment.CompanyAddress = request.POST["CompanyAddress"]
           numUpdates += 1
        try:
               
            if request.POST["CurrentlyWorking"] == 'OldCheck':
                pass
            if request.POST["CurrentlyWorking"] == 'on':
                employment.CurrentlyWorking = True
                numUpdates += 1
        except:
            employment.CurrentlyWorking = False
            numUpdates += 1
    
        
           
        if request.POST["Telephone"]:
           employment.Telephone = request.POST["Telephone"]
           numUpdates += 1
           
        if request.POST["WorkPosition"]:
           employment.WorkPosition = request.POST["WorkPosition"]
           numUpdates += 1
           
        if request.POST["StartDate"]:
           employment.StartDate = request.POST["StartDate"]
           numUpdates += 1
        if request.POST["EndDate"]:
           employment.EndDate = request.POST["EndDate"]
           numUpdates += 1
        if request.POST["Skills"]:
           employment.Skills = request.POST["Skills"]
           numUpdates += 1
        
        if numUpdates >0:
            
            employment.save()
            messages.success(request,"You have updated the employment information successfully")
        else:
            messages.error(request, "You did not make any changes on the record")
        
        return redirect('updateEmployment',employmentId=employment.Employment_id, place=place)    
        
        
        
#removing employment information
@login_required
def removeEmployment(request, employmentId, place):
    employment = get_object_or_404(Employment, pk=employmentId)
    person= employment.personId
    
    if request.method =='GET':
        messages.error(request, "Are you sure you want to remove this record")
        return render(request, 'ManagePersonal/removeEmployment.html',{"employment":employment,"person":person,"place": place,"Person":person})
    
    if request.method =='POST':
        
        employment.delete()
        messages.success(request,"You have removed the employment information successfully")
        
    if place=="OnCreate":
        return redirect('addEmployment',personId = person.personId)  
    
        
        
#adding the doctors information
@login_required
def addDoctor(request, personId):
    
    person = get_object_or_404(Persons, pk=personId)
    prof = checkProfiles(person)
    if request.method == 'GET':
        
        return render(request, 'ManagePersonal/addDoctor.html',{"prof":prof,"person":person})
    
    if request.method =="POST":
        
        Doctor = Doctorsinformation.objects.create(
            
            FirstName = request.POST["FirstName"],
            Surname = request.POST["Surname"],
            Speciality = request.POST["Speciality"],
            Role = request.POST["Role"],
            CellNumber = request.POST["CellNumber"],
            EmailAddress = request.POST["EmailAddress"],
            WorkAddress = request.POST["WorkAddress"],
            WorkTel = request.POST["WorkTel"],
            personId = person
        )
        
        messages.success(request, "We are done with the personal information please select a profile to create")
        messages.warning(request,"please double check these details, correct and/or continue.")
        return redirect('updateDoctor',docId=Doctor.DoctorsId, place="OnCreate")
    
#upating doctors information

@login_required
def updateDoctor(request, docId,place):
    
    Doctor = get_object_or_404(Doctorsinformation, pk=docId)
    person = Doctor.personId
    
    if request.method == 'GET':
          
        return render(request,'ManagePersonal/updateDoctor.html',{"Doctor":Doctor,"person":person,"place":place})
    
    if request.method == 'POST':
        
        numUpdates = 0
        
        if request.POST["FirstName"]:
            Doctor.FirstName = request.POST["FirstName"]
            numUpdates += 1
             
        
        if request.POST["Surname"]:
            Doctor.Surname = request.POST["Surname"]
            numUpdates += 1
            
        if request.POST["Speciality"]:
            Doctor.Speciality = request.POST["Speciality"]
            numUpdates += 1
            
        if request.POST["Role"]:
            Doctor.Role = request.POST["Role"]
            numUpdates += 1
            
        if request.POST["CellNumber"]:
            Doctor.CellNumber = request.POST["CellNumber"]
            numUpdates += 1
            
        if request.POST["EmailAddress"]:
            Doctor.EmailAddress = request.POST["EmailAddress"]
            numUpdates += 1
            
        if request.POST["WorkAddress"]:
            Doctor.WorkAddress = request.POST["WorkAddress"]
            numUpdates += 1
    
        if request.POST["WorkTel"]:
            Doctor.WorkTel = request.POST["WorkTel"]
            numUpdates += 1
            
        if numUpdates > 0:
            Doctor.save()
            messages.success(request, "You have successfully updated the doctors record")
        else:
            messages.error(request, "You did not make any changes on the record")
            
        return redirect('updateDoctor',docId = Doctor.DoctorsId, place = place)
            
def ToChoose(request, id):
    user = request.user
    p = get_object_or_404(Persons,user = user)
    isParent =  checkParent(p)
    if request.method =='GET':
        return render(request, 'manageProfile/ChooseProfile.html',{"person":id,"isParent":isParent})  
        
    
    
   
#Adding CustomField
@login_required
def addCustomField(request, personId, place):
    user = request.user
    person = get_object_or_404(Persons, pk = personId)
    ParentPersonID = 0
    if request.method == 'GET':
        fields = getFieds(person)
        try:
            if request.session['process']:
                if request.session["process"] =="Parent":
                    p = get_object_or_404(Persons, user = user)
                    ParentPersonID = p.personId
        except:
            pass            
        
        print(f"Custome fields length: {len(fields)}")
        
        return render(request,'ManagePersonal/addCustomField.html',{"person":person,"fields":fields,"place":place, "ParentPersonID":ParentPersonID,"length":len(fields)}) 

    if request.method =='POST':
        
        customfeild = CustomField.objects.create(
            personId = person,
            FeildName = request.POST["FeildName"],
            FeildValue = request.POST["FeildValue"],
            
        )
        
        messages.success(request,"Feild added successsfully you may add more")
        
        return redirect('addCustomField', personId, place)
   
#getting all cunstom fields

def getFieds(person):
    fields = []
    Cs = CustomField.objects.all()
    for item in Cs:
        if item.personId == person:
            fields.append(item)
    return fields
    
  
  
#Updating custom fields
@login_required
def updateCustomField(request, fieldID, place):
    customField = get_object_or_404(CustomField, pk = fieldID)
    
    if request.method == 'GET':
        
        
        return render(request, 'ManagePersonal/updateCustomField.html', {"customField": customField, "place":place})
    
    if request.method == 'POST':
        numUpdates = 0
        if request.POST["FeildName"] != customField.FeildName:
            customField.FeildName = request.POST["FeildName"]
            numUpdates += 1
            
        if request.POST["FeildValue"] != customField.FeildValue:
            customField.FeildValue = request.POST["FeildValue"]
            numUpdates += 1
        if numUpdates > 0:
            customField.save()
            messages.success(request, "changes to the field have been made successfully")
        else:
            messages.error(request,"You did not make any changes on the record")
        print("did")
        return redirect('updateCustomField', fieldID = customField.FeildId,place = request.POST["place"])            
            
            
            
#removing  CustomField
def removeCustomField(request, customField, place):
    
    f = get_object_or_404(CustomField, pk = customField)
    personId = f.personId.personId
    
    if request.method== 'GET':
        f.delete()
        print(f"The plce is {place}")
        
        messages.success(request, "Field removed successfully")
        
        if place == "OnCreate":
            return redirect('addCustomField',personId =personId, place=place)
        if place == "OnView":
            return redirect('viewPerson',default="Person",AtheId=0)
    
            
            
     
    
    
def checkProfiles(person):
   
    prof = False
    p= views.getProfiles(person.personId, "nothing")
   
    profNum = 0
    for item in p:
        profNum +=1
    if profNum > 0:
        prof = True
    
    return prof
    

        
        