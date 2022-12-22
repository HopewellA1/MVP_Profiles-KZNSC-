from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from .models import Athlete,Persons,Parent
from django.utils.dateparse import parse_date
from datetime import date, datetime
from django.contrib.auth.decorators import login_required

@login_required
def personal(request, id):
    user = request.user
    if request.method == 'GET':
        return render(request,'manageProfile/Personal.html', {"parent": id})
    if request.method == 'POST':
        
        
       
        if id != "0":
            Person = Persons.objects.create(IdentityNumber = request.POST['IdentityNumber'],FirstName = request.POST['FirstName'])
            p = Persons.objects.get(IdentityNumber = Person.IdentityNumber)
            ParentPerson = get_object_or_404(Persons, pk = id)
            
            #parent = get_object_or_404(Parent, personId = Person)
            messages.success(request,f"Dear { ParentPerson.FirstName}, Athlate personal information saved successfully please continue adding the required information below")
            return redirect('creatProfile', id=p.personId, profile="Parent",parent=ParentPerson.personId)
        else:
            Person = Persons.objects.create(IdentityNumber = request.POST['IdentityNumber'],FirstName = request.POST['FirstName'], user = user)
            p = Persons.objects.get(IdentityNumber = Person.IdentityNumber)
            
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
@login_required
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

        return render(request, 'manageProfile/CreateProfile.html',{"profile":prof, "parent":parent})
    if request.method=='POST':
        
        #creating athlate instance
        ProfDefault = False
        if profile =="Parent":
            pass
        else:
            parent = "0"
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
            ParentPerson = get_object_or_404(Persons, pk = request.POST["parent"])
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


@login_required
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
        messages.success(request,f"Dear {Person.FirstName} please add your athlate personal information")
        #return render(request,'manageProfile/home.html',{"parent":parent, "ParentPerson":Person.personId})
        #return redirect('creatProfile', id=Person.personId, profile="Parent")
        return redirect('personal', id=Person.personId)
    
    
    
    
    
    
    
    
    
@login_required    
def ViewInformation(request,id, profile):
 
    prof =profile
    t = profile
    Person = get_object_or_404(Persons, pk = id)
    
    if profile =="Athlate":
     
        prof = get_object_or_404(Athlete,pk = Athlete.objects.get(personId = Person).AthleteID)
    
    if request.method == 'GET':
   
        return render(request, 'manageProfile/ViewInfo.html',{"person":Person, "profile":prof,"type":profile})
    if request.method =='POST':
       
        if request.POST["profiletype"] =="Athlate":
            NumUpdate = 0
            athlete = get_object_or_404(Athlete,personId= Person)
          
           # athlete = Athlete.objects.get(personId = Person)
            if request.POST['Federation']:
                if request.POST['Federation'] ==  "Select":
                    pass
                else:
                    athlete.Federation = request.POST['Federation']
                    NumUpdate += 1
            if request.POST['AthleteLevel']:
                athlete.AthleteLevel = request.POST['AthleteLevel']
                NumUpdate += 1
            if request.POST['ClubName']:
                athlete.ClubName = request.POST['ClubName']
                NumUpdate += 1
            if request.POST['ClubLevel']:
                athlete.ClubLevel = request.POST['ClubLevel']
                NumUpdate += 1
            if request.POST['ClubLevel']:
                athlete.ClubLevel = request.POST['ClubLevel']
                NumUpdate += 1 
            
            if request.POST['PlayerType']:
                athlete.PlayerType = request.POST['PlayerType']
                NumUpdate += 1  
            try:
                if request.FILES['ProfileImage']:
                    athlete.ProfileImage=request.FILES['ProfileImage']
                    NumUpdate += 1    
            except:
                pass
            
            if NumUpdate >0:
                print(f"\n\nNumber of updates made: {NumUpdate} \n\n")
                messages.success(request,f"Profile information has been updated successfully")
                
                athlete.save()
            else:
                messages.success(request,f"Dear {Person.FirstName} you did not make any changes on your profile")
                
            return redirect('ViewInformation', id=Person.personId, profile="Athlate")
           
        return render(request, 'manageProfile/ViewInfo.html',{"person":Person, "profile":prof,"type":profile})


#the following Action method get the parent profile for the curent user if they have a parent profile.
@login_required
def viewParent(request):
    
    if request.method == 'GET':
        Athletes = []
        user = request.user
        personalinfo = get_object_or_404(Persons, user = user)
        if personalinfo.NumProfile >1:
            #get all the profiles belonging to that person
            pass
        print(personalinfo)
        parentProfile = get_object_or_404(Parent,personId = personalinfo)
        athleteProfiles = Athlete.objects.get(ParentId = parentProfile)
        # For the for statement we need to call an internal api for getting the athlets by parent id if posible
        for athlete in athleteProfiles:
            
            athletePersonalInfo = get_object_or_404(Persons, pk = athlete.personId)
            athleteView = {
                "FirstName": athletePersonalInfo.FirstName,
                "ProfileImage": athlete.ProfileImage,
                "PersonId":athletePersonalInfo.personId,
                
            }
            Athletes.append(athleteView)
            
        print(
            "The profiles associated with parent are as follows.\n\n"
            +f"Current user: {user}\n Perent personal Info: {personalinfo.FirstName}"
            +f"\nAthlets under the parent: {Athletes}"
        )
        return render(request, 'manageProfile/viewParent.html',
                      {"ParentPerson":personalinfo, "ParentProfile": parentProfile, "Athlets": Athletes})
    
    

