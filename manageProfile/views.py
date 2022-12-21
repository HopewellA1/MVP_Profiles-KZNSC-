from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from .models import Athlete,Persons,Parent
from django.utils.dateparse import parse_date
from datetime import date, datetime

def personal(request, id):
    if request.method == 'GET':
        return render(request,'manageProfile/Personal.html', {"parent": id})
    if request.method == 'POST':
        Person = Persons.objects.create(IdentityNumber = request.POST['IdentityNumber'],FirstName = request.POST['FirstName'])
        p = Persons.objects.get(IdentityNumber = Person.IdentityNumber)
        
        print(p.personId)
        if id != "0":
            ParentPerson = get_object_or_404(Persons, pk = id)
            
            #parent = get_object_or_404(Parent, personId = Person)
            messages.success(request,f"Dear { ParentPerson.FirstName}, Athlate personal information saved successfully please continue adding the required information below")
            return redirect('creatProfile', id=p.personId, profile="Parent",parent=ParentPerson.personId)
            
            
        return render(request, 'manageProfile/ChooseProfile.html',{"person": p.personId})

def home(request):

    if request.method == 'GET':
        return render(request,'manageProfile/home.html')
    if request.method == 'POST':
        Person = Persons.objects.create(IdentityNumber = request.POST['IdentityNumber'],FirstName = request.POST['FirstName'])
        p = Persons.objects.get(IdentityNumber = Person.IdentityNumber)
        
        print(p.personId)
        if request.POST["parent"]:
            ParentPerson = get_object_or_404(Persons, pk = request.POST['person'])
            #parent = get_object_or_404(Parent, personId = Person)
            messages.success(f"Dear { ParentPerson.FirstName}, Athlate personal information saved successfully please continue adding the required information below")
            return redirect('creatProfile', id=Person.personId, profile="Parent")
            
            
        return render(request, 'manageProfile/ChooseProfile.html',{"person": p.personId})

def chooseProfile(request):
    if request.method == 'GET':
        return render(request, 'manageProfile/ChooseProfile.html')
    if request.method == 'POST':

        Person = get_object_or_404(Persons, pk = request.POST['person'])
        return redirect('creatProfile', id=Person.personId, profile="Athlate")
       # return render(request, 'manageProfile/CreateProfile.html',{"person": Person.personId})

def creatProfile(request,id, profile, parent):
    prof =''
    
    if request.method =="GET":
        try:
            #if a person alredy has that profile we will let them know
            if profile =="Athlate":
                prof = Athlete.objects.get(personId = id)
            if profile =="Parent":
                prof = Parent.objects.get(personId = id)
                
        except:
            # if they don't have any of the above we let them continue to create
            pass

        return render(request, 'manageProfile/CreateProfile.html',{"profile":prof, "parent":prof})
    if request.method=='POST':
        
        #creating athlate instance
        ProfDefault = False
        if profile =="Parent":
            pass
        Person = get_object_or_404(Persons, pk = id)
        if Person.NumProfile == 0:
           ProfDefault = True
        else:
            ProfDefault = False
        athlete = Athlete.objects.create(personId = Person,
                                        ProfileImage=request.FILES['ProfileImage'],
                                         Federation = request.POST['Federation'],
                                         PlayerType = request.POST['PlayerType'],
                                         AthleteLevel = request.POST['AthleteLevel'],
                                         ClubName = request.POST['ClubName'],
                                         ClubLevel = request.POST['ClubLevel'],
                                         JoinDate = datetime.now(),
                                         Default = ProfDefault,
                                        
                                             
                                         )
        if parent !="0":
            Ath =get_object_or_404(Athlete,personId = Person)
            ParentPerson = get_object_or_404(Persons, pk = parent)
            AthlateParent = get_object_or_404(Parent, personId = ParentPerson)
            Ath.ParentId = AthlateParent
            Ath.save()
            #athlete.
        Person.NumProfile += 1
        Person.save()

        print(f"The new athlete object: {athlete}")
        if profile =="Athlate":
                prof = Athlete.objects.get(personId = id)


       # person = Persons.objects.get()
        #athlate = Athlete.objects.create()
        return redirect('ViewInformation', id=Person.personId, profile="Athlate")
       # return render(request, 'manageProfile/CreateProfile.html',{"profile":prof})






def ParentInfo(request,id ):
    Person = get_object_or_404(Persons, pk = id)
    try:
        parentProfile = Parent.objects.get(personId = id)
        if parentProfile:
            #redirect back to choose profile if parent profile exists
            pass
    except:
        pass
    ProfDefault = False
    if Person.NumProfile == 0:
        ProfDefault = True
    else:
        ProfDefault = False
    if request.method =='GET':
        #messages.success(f"Dear {Person.FirstName} please add your profile image")# shall add Other information if will be later required
        return render(request, 'manageProfile/ParentInfo.html',{"person":Person})
    if request.method == 'POST':
       
        Person = get_object_or_404(Persons, pk = id)
        parent = Parent.objects.create(personId = Person,
                                        ProfileImage=request.FILES['ProfileImage'],
                                         
                                        JoinDate = datetime.now(),
                                        Default = ProfDefault
                                         )
        Person.NumProfile += 1
        Person.save()
        #messages.success(f"Dear {Person.FirstName} please add your athlate personal information")
        #return render(request,'manageProfile/home.html',{"parent":parent, "ParentPerson":Person.personId})
        #return redirect('creatProfile', id=Person.personId, profile="Parent")
        return redirect('personal', id=Person.personId)
    
    
    
    
    
    
    
    
    
    
def ViewInformation(request,id, profile):
    print(f"The prifile type is:{profile} on normal")
    prof =profile
    t = profile
    Person = get_object_or_404(Persons, pk = id)
    
    if profile =="Athlate":
     
        prof = get_object_or_404(Athlete,pk = Athlete.objects.get(personId = Person).AthleteID)
    
    if request.method == 'GET':
        print(f"The prifile type is:{profile} on Get")
        return render(request, 'manageProfile/ViewInfo.html',{"person":Person, "profile":prof,"type":profile})
    if request.method =='POST':
        print(f"The prifile type is:{t} on Post")
        if request.POST["profiletype"] =="Athlate":
            
            athlete = get_object_or_404(Athlete,personId= Person)
            print(f"The new Atthlate is now: {athlete}")
           # athlete = Athlete.objects.get(personId = Person)
            if request.POST['Federation']:
                athlete.Federation = request.POST['Federation']
            if request.POST['AthleteLevel']:
                athlete.AthleteLevel = request.POST['AthleteLevel']
            if request.POST['ClubName']:
                athlete.ClubName = request.POST['ClubName']
            if request.POST['ClubLevel']:
                athlete.ClubLevel = request.POST['ClubLevel']
            if request.POST['ClubLevel']:
                athlete.ClubLevel = request.POST['ClubLevel']  
            if request.FILES['ProfileImage']:
                athlete.ProfileImage=request.FILES['ProfileImage']
                
            messages.success(request,f"Dear {Person.FirstName} your profile information has been updated successfully")
            athlete.save()
            return redirect('ViewInformation', id=Person.personId, profile="Athlate")
           
        return render(request, 'manageProfile/ViewInfo.html',{"person":Person, "profile":prof,"type":profile})







