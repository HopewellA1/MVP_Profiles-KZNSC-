import json
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import Athlete,Parent,Coach,Official,Achievement
from django.utils.dateparse import parse_date
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
#from .serialization import Serializationclass
#from rest_framework import generics,filters#,viewsets
#from rest_framework.response import Response
from ManagePersonal.views import getEducation,getEmployment,checkParent, getFieds
from ManagePersonal.models import Persons,Nextofkin,Education,Employment,Doctorsinformation



def home(request):

    if request.method == 'GET':
        person =""
        if request.user:
            user = request.user
            try:
                person = get_object_or_404(Persons,user = user)
            except:
                pass
        
        return render(request,'manageProfile/home.html',{"person":person})
    # if request.method == 'POST':
    #     Person = Persons.objects.create(IdentityNumber = request.POST['IdentityNumber'],FirstName = request.POST['FirstName'])
    #     p = Persons.objects.get(IdentityNumber = Person.IdentityNumber)
        
    #     print(p.personId)
    #     if request.POST["parent"]:
    #         ParentPerson = get_object_or_404(Persons, pk = request.POST['person'])
    #         #parent = get_object_or_404(Parent, personId = Person)
    #         messages.success(f"Dear { ParentPerson.FirstName}, Athlate personal information saved successfully please continue adding the required information below")
    #         return redirect('creatProfile', id=Person.personId, profile="Parent")
            
            
    #     return render(request, 'manageProfile/ChooseProfile.html',{"person": p.personId})
@login_required
def chooseProfile(request):
    user = request.user
    p = get_object_or_404(Persons, user = user)
    isParent =  checkParent(p)
    if request.method == 'GET':
        return render(request, 'manageProfile/ChooseProfile.html',{"isParent":isParent,"person":p.personId,"p":p})
    
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
                messages.success(request,f"Dear { prof.personId.FirstName}, Athlate personal information saved successfully please continue adding the required information below")
            
                
        except:
            # if they don't have any of the above we let them continue to create
            pass
        try:
            if request.session['process']:
                if request.session["process"] =="Parent":
                    
                    p = get_object_or_404(Persons, pk = parent)
                    messages.success(request,f"Dear , {p.FirstName} Athlate personal information saved successfully please continue adding the required information below")
        except:
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
        print(f"\n\nThe person of the athlete profile object is :{Person}")
        if Person.NumProfile == 0:
           ProfDefault = True
        else:
            ProfDefault = False
        Athlete.objects.create(personId = Person,
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
           
            #Ath.personId = Person
            
            ParentPerson = get_object_or_404(Persons, pk = request.POST["parent"])
            AthlateParent = get_object_or_404(Parent, personId = ParentPerson)
            Ath.ParentId = AthlateParent
         
            Ath.save()
            #athlete.
        Person.NumProfile += 1
        Person.save()

        request.session['process'] = None
        
        prof = Athlete.objects.get(personId = Person)


       # person = Persons.objects.get()
        #athlate = Athlete.objects.create()
       
        return redirect('addAchievements',profileId = prof.AthleteID,type="Athlete",place="OnCreate")
       
        return redirect('viewPerson', default="Athlete",AtheId=0)
       
       
       
       
       # return redirect('ViewInformation', id=Person.personId, profile="Athlate")
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
        newP = get_object_or_404(Parent, personId = Person)
        
        
        #return render(request,'manageProfile/home.html',{"parent":parent, "ParentPerson":Person.personId})
       # return redirect('creatProfile', id=Person.personId, profile="Parent",parent=newP.ParentId)
        return redirect('personal', id=Person.personId)
     
    
    
@login_required    
def ViewInformation(request,id, profile):
 
    prof =profile
  
    Person = get_object_or_404(Persons, pk = id)
    
    if profile =="Athlate":
        pass
     
    prof = get_object_or_404(Athlete,personId = Person)
    
    if request.method == 'GET':
   
        return render(request, 'manageProfile/ViewInfo.html',{"person":Person, "profile":prof,"type":profile})
    if request.method =='POST':
       
        #if request.POST["profiletype"] =="Athlate":
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
            try:
                    if request.POST["Default"] == 'on':
                    
                        for item in getProfiles(Person.personId,remove="Athlete"):
                            obj = item["Profile"]
                        
                            if obj.Default == True:
                                if item["type"] =="Parent":
                                    parent = get_object_or_404(Parent, pk = obj.ParentId)
                                    parent.Default = False
                                    parent.save()
                                    print(f"Current default: {parent.Default}")
                                if item["type"] =="Athlete":
                                    athlete = get_object_or_404(Athlete, pk = obj.AthleteID)
                                    athlete.Default = False
                                    athlete.save()
                                    print(f"Current default: {athlete.Default}")
                                if item["type"]  =="Coach":
                                    coach = get_object_or_404(Coach, pk = obj.CoachID)
                                    coach.Default = False
                                    coach.save()
                                    print(f"Current default: {coach.Default}")
                                if item["type"]  =="Official":
                                    official = get_object_or_404(Official, pk = obj.CoachID)
                                    official.Default = False
                                    official.save()
                                    print(f"Current default: {official.Default}")
                                    
                        
                        athlete.Default =True 
                        NumUpdate += 1             
            except:
                pass    
             
            
            
            name =""
            if request.POST["profiletype"] =="Parent":
           
                name  = athlete.ParentId.personId.FirstName
            if request.POST["profiletype"] =="Athlete":
                if NumUpdate == 0:
                    name = Person.FirstName
                else:
                    name = f"{Person.FirstName} your"
            if NumUpdate >0:
                print(f"\n\nNumber of updates made: {NumUpdate} \n\n")
                messages.success(request,f"Dear {name} profile information has been updated successfully")
                
                athlete.save()
            else:
                messages.success(request,f"Dear {name} you did not make any changes to the profile")
                
            return redirect('ViewInformation', id=Person.personId, profile=request.POST["profiletype"])
           
        #return render(request, 'manageProfile/ViewInfo.html',{"person":Person, "profile":prof,"type":profile})


#the following Action method get the parent profile for the curent user if they have a parent profile.
@login_required
def viewPerson(request, default,AtheId):
    #ParentAthlete
    #Athlete
    #Parent
    #Official
    #Person
    #
    user = request.user
    ParentAthlete = False
    AllAchievements = []
    if request.method == 'GET':
        Athletes = []
        Default = ""
        
        numProf = 0
        education =""
        allPersonProfiles = []
        if default == "ParentAthlete" or int(AtheId) > 0:
            AthleteProfile = get_object_or_404(Athlete,pk =AtheId)
            personalinfo = AthleteProfile.personId
            eds = getEducation(personalinfo)
            employments = getEmployment(personId=personalinfo.personId) 
            nextOfKin = get_object_or_404(Nextofkin, personId = personalinfo.personId)
            ParentAthlete = True
            
            
        else:
            personalinfo = get_object_or_404(Persons, user = user)
          
            eds = getEducation(personalinfo)
            employments = getEmployment(personId=personalinfo.personId) 
            nextOfKin = get_object_or_404(Nextofkin, personId = personalinfo.personId)
            try:
                education = get_object_or_404(Education,personId = personalinfo)
            except:
                pass
        
        # getting all profile belonging to the person using try 
        try:
            #starting with parent profile
            parentProfile = get_object_or_404(Parent,personId = personalinfo)
            athleteProfiles = Athlete.objects.all()
            for athlete in athleteProfiles:
           
                pass
                # athletePersonalInfo = get_object_or_404(Persons, pk = athlete.personId)
            
                if athlete.ParentId == parentProfile:
                    #AthPerson = get_object_or_404(Persons,personId= athlete.personId)
                    athleteView = {
                    "FirstName": athlete.personId.FirstName,
                    "ProfileImage": athlete.ProfileImage,
                    "PersonId":athlete.personId.personId,
                    "profile":athlete
                    
                }
                    Athletes.append(athleteView)
                    numProf +=1
            
            
       
         
            if parentProfile.Default == True:
                DefaultProfile = parentProfile
                Default = "Parent"
                
                
            pr = { "type": "Parent",
                    "Default": parentProfile.Default,
                    "pl":parentProfile
                  }
            if parentProfile.Status == "Active":
                allPersonProfiles.append(pr)
                numProf +=1
                
            
            
        except:
       
            pass
        
        try:
            
            #up next is the Athlete profile
            athletetProfile = get_object_or_404(Athlete,personId = personalinfo)
            if athletetProfile.Default == True:
                DefaultProfile = athletetProfile
                Default = "Athlete"
            pr = { "type": "Athlete",
                    "Default": athletetProfile.Default,
                    "pl":athletetProfile,
                    "id":athletetProfile.AthleteID
                  }
            if athletetProfile.Status == "Active":
                allPersonProfiles.append(pr)
                numProf +=1
            AllAchievements = getAchievement(athletetProfile.AthleteID,Default)
            pass
        except:
            pass
        print(f"Default is : {Default}")
        try:
            #fight goes on we on Coach profile
            coachProfile = get_object_or_404(Coach,personId = personalinfo)
            if coachProfile.Default == True:
                DefaultProfile = coachProfile
                Default = "Coach"
            
            pr = { "type": "Coach",
                    "Default": coachProfile.Default,
                    "pl":coachProfile,
                    "id":coachProfile.CoachID
                  }
            if coachProfile.Status == "Active":
                allPersonProfiles.append(pr)
            AllAchievements = getAchievement(coachProfile.CoachID,Default)
        except:
            pass
        
        
        try:
            #cant't stop now we go with Official profile
            officialProfile = get_object_or_404(Official,personId = personalinfo)
            if officialProfile.Default == True:
                DefaultProfile = officialProfile
                Default = "Official"
            
            pr = { "type": "Official",
                    "Default": officialProfile.Default,
                    "pl":officialProfile,
                    "id":officialProfile.OfficialID
                  }
            if officialProfile.Status == "Active":
                allPersonProfiles.append(pr)
            AllAchievements = getAchievement(officialProfile.OfficialID,Default)
        except:
            pass
        
        fields = []     
        for item in allPersonProfiles:
         
         
            if item["type"] == default:
                
            
                if default == "Parent":
                    AllAchievements = []
                else:
                    AllAchievements = getAchievement(item["id"],item["type"])
                return render(request, 'manageProfile/viewPerson.html',
                    {
                         "Person":personalinfo,
                         "DefaultProfile": item["pl"],
                         "Athlets": Athletes,
                         "Default":default,
                         "allPersonProfiles":allPersonProfiles,
                         "education":education,
                         "eds":eds,
                         "employments":employments,
                         "AllAchievements":AllAchievements,
                         "ParentAthlete":ParentAthlete
                      
                         
                    }) 
         #NextOfKin  
           
        if default == "Person":
            fields =getFieds(personalinfo)
            Default =  default
            AllAchievements =[]
        if default == "Education":
            Default = default
            AllAchievements =[]
        if default == "Employment":
            Default = default
            AllAchievements =[]
        if default == "NextOfKin":
            Default = default
            AllAchievements =[]
        return render(request, 'manageProfile/viewPerson.html',
                        {"Person":personalinfo,
                         "DefaultProfile": DefaultProfile,
                         "Athlets": Athletes,
                         "Default":Default,
                         "allPersonProfiles":allPersonProfiles,
                         "education":education,
                         "eds":eds,
                         "employments":employments,
                         "nextofkin":nextOfKin,
                         "AllAchievements":AllAchievements,
                         "ParentAthlete":ParentAthlete,
                         "fields":fields
                         })
       
            
     
       
#Now creating Coach Profile
@login_required
def CreateCoach(request,id):
    user = request.user
    PersonInfo = get_object_or_404(Persons, user = user)
   
    #Checking if the person has a coach profile
    try:
        coach = get_object_or_404(Coach,personId = PersonInfo)
    except:
        #if we do no get it we let them pass to create the profile, As i do not know if they are allowed to create more than one profile of coach
        pass 
    if request.method == 'GET':
        
        return render(request, 'manageProfile/CreateCoach.html',{"person":PersonInfo}) 
    
    if request.method == 'POST':
        ProfDefault = False
        
        Person = PersonInfo
        if Person.NumProfile == 0:
           ProfDefault = True
        else:
            ProfDefault = False
        coach = Coach.objects.create(personId = Person,
                                        ProfileImage=request.FILES['ProfileImage'],
                                         Federation = request.POST['Federation'],
                                       
                                         CoachLevel = request.POST['CoachLevel'],
                                         ClubName = request.POST['ClubName'],
                                   
                                         JoinDate = datetime.now(),
                                         Default = ProfDefault,
                                        
                                             
        )
        Person.NumProfile += 1
        Person.save()
        messages.success(request,f"Dear {coach.personId.FirstName} you have succeessfully created the coach profile")
        return redirect('addAchievements',profileId = coach.CoachID,type="Coach",place="OnCreate")
        return redirect('viewPerson', default = "Coach",AtheId = 0)
    
    
    

@login_required
def updateCoach(request,PersonId, CoachId):
    CoachPerson = get_object_or_404(Persons, pk= PersonId)
    coachProfile = get_object_or_404(Coach, personId = CoachPerson)
    
    if request.method == 'GET':
        return render(request, 'manageProfile/updateCoach.html', {"coach": coachProfile,"CoachPerson":CoachPerson,"type": "Coach"})
    
    if request.method =='POST':
        
        NumUpdate = 0
        coach = get_object_or_404(Coach,personId= CoachPerson)
    
        if request.POST['Federation']:
            if request.POST['Federation'] ==  "Select":
                pass
            else:
                coach.Federation = request.POST['Federation']
                NumUpdate += 1
                
        if request.POST['CoachLevel']:
            coach.CoachLevel = request.POST['CoachLevel']
            NumUpdate += 1
                
        if request.POST['ClubName']:
            coach.ClubName = request.POST['ClubName']
            NumUpdate += 1      
        
        try:
            if request.FILES['ProfileImage']:
                coach.ProfileImage=request.FILES['ProfileImage']
                NumUpdate += 1    
        except:
            pass
        try:
            if request.POST["Default"] == 'on':
             
                for item in getProfiles(CoachPerson.personId, remove= "Coach"):
                    obj = item["Profile"]
                   
                    if obj.Default == True:
                        if item["type"] =="Parent":
                            parent = get_object_or_404(Parent, pk = obj.ParentId)
                            parent.Default = False
                            parent.save()
                            print(f"Current default: {parent.Default}")
                        if item["type"] =="Athlete":
                            athlete = get_object_or_404(Athlete, pk = obj.AthleteID)
                            athlete.Default = False
                            athlete.save()
                            print(f"Current default: {athlete.Default}")
                        if item["type"]  =="Coach":
                            coach = get_object_or_404(Coach, pk = obj.CoachID)
                            coach.Default = False
                            coach.save()
                            print(f"Current default: {coach.Default}")
                        if item["type"]  =="Official":
                            official = get_object_or_404(Official, pk = obj.CoachID)
                            official.Default = False
                            official.save()
                            print(f"Current default: {official.Default}")
                        
                      
                coach.Default =True 
                NumUpdate += 1     
                 
               # print(f"Profiles under the current person:\n\n{profiles}\n\n")
            #print(f"\n\nThe curent default value is: "+ request.POST["Default"] +"\n\n")
        except:
            pass
           
        if NumUpdate >0:
                #print(f"\n\nNumber of updates made: {NumUpdate} \n\n")
                messages.success(request,f"Dear {CoachPerson.FirstName} profile information has been updated successfully")
                
                coach.save()
        else:
            messages.success(request,f"Dear {CoachPerson.FirstName}  you did not make any changes to the profile")
        
        #return render(request, 'manageProfile/updateCoach.html', {"coach": coach,"CoachPerson":CoachPerson,"type": "Coach"})
        return redirect('updateCoach', PersonId=CoachPerson.personId, CoachId=coach.CoachID)
    
    
#updating parent profile which only hass profile image at the moment
@login_required
def updateParent(request, parentId):
    parentProfile = get_object_or_404(Parent, pk = parentId)
    parentPerson = parentProfile.personId
   # allProfiles = getProfiles(parentProfile.personId.personId, remove="none")
    if request.method =='GET':
      
        
        return render(request,'manageProfile/updateParent.html',{"parentProfile":parentProfile,"parentPerson":parentPerson,"type":"Parent"})
    
    if request.method =='POST':
        NumUpdate = 0
        try:
            if request.FILES['ProfileImage']:
                parentProfile.ProfileImage=request.FILES['ProfileImage']
                NumUpdate += 1    
        except:
            pass
    
        try:
            if request.POST["Default"] == 'on':
             
                for item in getProfiles(parentPerson.personId, remove = "Parent"):
                    obj = item["Profile"]
                   
                    if obj.Default == True:
                        if item["type"] =="Parent":
                            parent = get_object_or_404(Parent, pk = obj.ParentId)
                            parent.Default = False
                            parent.save()
                        if item["type"] =="Athlete":
                            athlete = get_object_or_404(Athlete, pk = obj.AthleteID)
                            athlete.Default = False
                            athlete.save()
                        if item["type"] =="Coach":
                            coach = get_object_or_404(Coach, pk = obj.CoachID)
                            coach.Default = False
                            coach.save()
                        if item["type"]  =="Official":
                            official = get_object_or_404(Official, pk = obj.CoachID)
                            official.Default = False
                            official.save()
                            print(f"Current default: {official.Default}")
                        
                      
                parentProfile.Default =True 
                NumUpdate += 1    
                 
            
        except:
            print("\n\nWe had error on the default parameter\n\n")
           
        
        
        
        
        
        
        if NumUpdate >0:
                print(f"\n\nNumber of updates made: {NumUpdate} \n\n")
                messages.success(request,f"Dear {parentPerson.FirstName} profile information has been updated successfully")
                
                parentProfile.save()
        else:
            messages.success(request,f"Dear {parentPerson.FirstName}  you did not make any changes to the profile")
        
        return redirect('updateParent', parentId=parentProfile.ParentId)
    

def getProfiles(Personid,remove):
    
    profiles =[]
    #ProfileObj ={}
    
    person = get_object_or_404(Persons, pk =Personid)
    
    #getParent
    if remove == "Parent":
       pass
    else:
        try:
            parent = get_object_or_404(Parent, personId = person)
            ProfileObj ={
                "Profile":parent,
                "type":"Parent"
            }
            if parent.Status == "Active":
                
                profiles.append(ProfileObj)
        except:
            pass
    
    #getAthlete
    if remove == "Athlete":
        pass
    else:
        try:
            athlete = get_object_or_404(Athlete, personId = person)
            ProfileObj ={
                "Profile":athlete,
                "type":"Athlete"
            }
            if athlete.Status == "Active":
                profiles.append(ProfileObj)
        except:
            pass
    
    #getCoach
    if remove == "Coach":
        pass
    else:
        

        try:
            coach = get_object_or_404(Coach, personId = person)
            ProfileObj ={
                "Profile":coach,
                "type":"Coach"
            }
            if coach.Status == "Active":
                profiles.append(ProfileObj)
        except:
            pass
    #get Official
    
    
    
    if remove == "Official":
        pass
    else:
        

        try:
            official = get_object_or_404(Official, personId = person)
            ProfileObj ={
                "Profile":official,
                "type":"Official"
            }
            if official.Status == "Active":
                profiles.append(ProfileObj)
        except:
            pass
    
    
    
    return profiles



#moving profile to deactivated in the name of delete

def remove(request, profId, type):
    t = type
    if type == "Parent":
        profile = get_object_or_404(Parent,pk =profId)
        
    if type == "Athlete":
        profile = get_object_or_404(Athlete,pk =profId)
        
    if type == "Coach":
        profile = get_object_or_404(Coach,pk =profId)
    
    if type == "Official":
        profile = get_object_or_404(Official,pk =profId)
    
    if request.method =='GET':
        if profile.Default == True:
            messages.success(request,"Please note that this is your default profile therefore you will have to select a new default below")
    
        Allprofiles = getProfiles(profile.personId.personId, remove = type)
        
        return render(request, 'manageProfile/remove.html',{"profile":profile,"person":profile.personId,"type":type,"Allprofiles":Allprofiles})
    
    if request.method == 'POST':
        
        try:
            #making a new default if the removed profile was a default one
            if request.POST["Default"]:
                newDefault = request.POST["Default"]
                if newDefault =="Parent":
                    parent = get_object_or_404(Parent,personId = profile.personId)
                    parent.Default = True
                    parent.save()
                if newDefault =="Athlete":
                    athlete = get_object_or_404(Athlete,personId = profile.personId)
                    athlete.Default = True
                    athlete.save()
                if newDefault =="Coach":
                    coach = get_object_or_404(Coach,personId = profile.personId)
                    coach.Default = True
                    coach.save()
                if newDefault =="Official":
                    official = get_object_or_404(Official,personId = profile.personId)
                    official.Default = True
                    official.save()
                pass
            pass
        except:
            pass
        
        profile.Default = False
        profile.Status = "Deactivated"
        profile.save()
        messages.success(request, f"Dear  {profile.personId.FirstName} you have removed the {t} profile suuccessfully")
        return redirect('viewPerson', default="none",AtheId=0)
        
#creating officals profile      
@login_required
def createOfficial(request):
    
    user = request.user
    PersonInfo = get_object_or_404(Persons, user = user)
    if request.method =='GET':
        
        
        return render(request,'manageProfile/createOfficial.html',{"person":PersonInfo})

    if request.method == 'POST':
        ProfDefault = False
        
        Person = PersonInfo
        if Person.NumProfile == 0:
           ProfDefault = True
        else:
            ProfDefault = False
        official = Official.objects.create(personId = Person,
                                        ProfileImage=request.FILES['ProfileImage'],
                                         Federation = request.POST['Federation'],
                                       
                                        
                                     
                                   
                                         JoinDate = datetime.now(),
                                         Default = ProfDefault,
                                         Position = request.POST["Position"],
                                        
                                             
        )
        Person.NumProfile += 1
        Person.save()
        messages.success(request,f"Dear {official.personId.FirstName} you have succeessfully created the official profile")
        return redirect('addAchievements',profileId = official.OfficialID,type="Official",place="OnCreate")
        return redirect('viewPerson', default = "Official",AtheId = 0)    
        
        
#updating Official profile
@login_required
def updateOfficial(request,PersonId):
    user = request.user
    OfficialPerson = get_object_or_404(Persons, user= user)
    officialProfile = get_object_or_404(Official, personId = OfficialPerson)
    if request.method =='GET':
        
        
        return render(request,'manageProfile/updateOfficial.html',{"OfficialPerson":OfficialPerson,"type":"Official","official":officialProfile})  
    
    if request.method =='POST':
        
        
          
        NumUpdate = 0
        official = get_object_or_404(Official,personId= OfficialPerson)
    
        if request.POST['Federation']:
            if request.POST['Federation'] ==  "Select":
                pass
            else:
                official.Federation = request.POST['Federation']
                NumUpdate += 1
                
       
                
        if request.POST['Position']:
            official.Position = request.POST['Position']
            NumUpdate += 1
        
        try:
            if request.FILES['ProfileImage']:
                official.ProfileImage=request.FILES['ProfileImage']
                NumUpdate += 1    
        except:
            pass
        try:
            if request.POST["Default"] == 'on':
             
                for item in getProfiles(OfficialPerson.personId, remove= "Official"):
                    obj = item["Profile"]
                   
                    if obj.Default == True:
                        if item["type"] =="Parent":
                            parent = get_object_or_404(Parent, pk = obj.ParentId)
                            parent.Default = False
                            parent.save()
                            print(f"Current default: {parent.Default}")
                        if item["type"] =="Athlete":
                            athlete = get_object_or_404(Athlete, pk = obj.AthleteID)
                            athlete.Default = False
                            athlete.save()
                            print(f"Current default: {athlete.Default}")
                        if item["type"]  =="Coach":
                            coach = get_object_or_404(Coach, pk = obj.CoachID)
                            coach.Default = False
                            coach.save()
                            print(f"Current default: {coach.Default}")
                        
                        if item["type"]  =="Official":
                            official = get_object_or_404(Official, pk = obj.CoachID)
                            official.Default = False
                            official.save()
                            print(f"Current default: {official.Default}")
                official.Default =True 
                NumUpdate += 1     
                 
               # print(f"Profiles under the current person:\n\n{profiles}\n\n")
            #print(f"\n\nThe curent default value is: "+ request.POST["Default"] +"\n\n")
        except:
            pass
           
        if NumUpdate >0:
                #print(f"\n\nNumber of updates made: {NumUpdate} \n\n")
                messages.success(request,f"Dear {OfficialPerson.FirstName} profile information has been updated successfully")
                
                official.save()
        else:
            messages.success(request,f"Dear {OfficialPerson.FirstName}  you did not make any changes to the profile")
        
        #return render(request, 'manageProfile/updateCoach.html', {"coach": coach,"CoachPerson":CoachPerson,"type": "Coach"})
        return redirect('updateOfficial', PersonId=OfficialPerson.personId)
    
        
        
        
        
#Adding Achievements
@login_required
def addAchievements(request, profileId, type, place):
    AllAchievements = getAchievement(profileId,type)
    if type =="Athlete":
        profile = get_object_or_404(Athlete, pk = profileId)
    if type =="Coach":
        profile = get_object_or_404(Coach, pk = profileId)
    if type =="Official":
        profile = get_object_or_404(Official, pk = profileId)
        
    if request.method == "GET":
        
        
        return render(request, 'manageProfile/addAchievements.html',{"profile":profile,"person":profile.personId,"type":type,"place":place,"AllAchievements":AllAchievements})
    
    
    
    if request.method =='POST':
        
        achievement = Achievement.objects.create(
            TypeOfAchievement = request.POST["TypeOfAchievement"],
            NameOfAchievement = request.POST["NameOfAchievement"],
            Organization = request.POST["Organization"],
            YearOfAchievement = request.POST["YearOfAchievement"],
            Certificate = request.POST["Certificate"],
            
            
        )
        a = achievement
        if type =="Athlete":
            profile = get_object_or_404(Athlete, pk = profileId)
            a.AthleteID = profile
            id = profile.AthleteID
        if type =="Coach":
            profile = get_object_or_404(Coach, pk = profileId)
            a.CoachID = profile
            id = profile.CoachID
        if type =="Official":
            profile = get_object_or_404(Official, pk = profileId)
            a.OfficialID = profile
            id = profile.OfficialID
        a.save()
        
        messages.success(request,"You have added the achievement successfully, you may add more if posible")
        
        return redirect('addAchievements', profileId = id, type =type,place =place)
        

#updating achievement
@login_required
def updateAchievement(request, id,type, place):
    achievement = get_object_or_404(Achievement,pk = id)
    profID  = getProfileID(achievement, type)
  
    if request.method =='GET':
        
        
        return render(request,'manageProfile/updateAchievement.html',{"achievement":achievement,"type":type,"place":place,"profile":profID})
    
    if request.method =='POST':
        
        
        numUpdates = 0
        if request.POST["NameOfAchievement"] != achievement.NameOfAchievement:
            achievement.NameOfAchievement = request.POST["NameOfAchievement"]
            numUpdates += 1
            
        if request.POST["TypeOfAchievement"] != achievement.TypeOfAchievement:
            achievement.TypeOfAchievement = request.POST["TypeOfAchievement"]
            numUpdates += 1
            
        if request.POST["Organization"] != achievement.Organization:
            achievement.Organization = request.POST["Organization"]
            numUpdates += 1
           
           
          # date_str = '09-19-2022'

            #date_object = datetime.strptime(date_str, '%m-%d-%Y').date()
           
        if request.POST["Certificate"] == achievement.Certificate:
            pass
        else:
            achievement.Certificate = request.POST["Certificate"]
            numUpdates += 1
            
        if numUpdates > 0:
            achievement.save()
           
        else:
            pass   
     
        print("\n\nAnother\n\n")
        print(achievement.YearOfAchievement)
        try:
            if request.POST["YearOfAchievement"] == achievement.YearOfAchievement:
                
                pass
            else:
                
                achievement.YearOfAchievement = request.POST["YearOfAchievement"]
                achievement.save()
                numUpdates += 1
        except:
            pass
        
        if request.POST["Certificate"] == achievement.Certificate:
            pass
        else:
            achievement.Certificate = request.POST["Certificate"]
            numUpdates += 1
            
        if numUpdates > 0:
            
            messages.success(request,f"Changes to {achievement.NameOfAchievement} made successfully.")
        else:
            messages.error(request,"No changes made on the record.")       
         
        return redirect('updateAchievement',id= achievement.AchievementId, type =type,place=place)





def getProfileID(Achievement, type):
    
    if type =="Athlete":
            profile = Achievement.AthleteID.AthleteID
            
    if type =="Coach":
        profile = Achievement.CoachID.CoachID
       
    if type =="Official":
        profile = Achievement.OfficialID.OfficialID
        
    return profile
    
#getting all achievements belonging to the profile
def getAchievement(id, type):
    achievements =[]
    As = Achievement.objects.all()
    for item in As:
        if type =="Athlete":
            profile = get_object_or_404(Athlete, pk = id)
            if item.AthleteID == profile:
                achievements.append(item)
        if type =="Coach":
            profile = get_object_or_404(Coach, pk = id)
            if item.CoachID == profile:
                achievements.append(item)
        if type =="Official":
            profile = get_object_or_404(Official, pk = id)
            if item.OfficialID == profile:
                achievements.append(item)
        
    
    return achievements 


#removing achievement
@login_required
def removeAchievement(request, id, type,place):
    achievement = get_object_or_404(Achievement,pk = id)
    profID  = getProfileID(achievement, type)
  
    if request.method =='GET':
        
        messages.warning(request,"Are you sure you want to remove this achievement record?")
        return render(request,'manageProfile/removeAchievement.html',{"achievement":achievement,"type":type,"place":place,"profile":profID})
    
    if request.method =='POST':
        achievement.delete()
        messages.success(request, "Achievement record removed successfully")
        if place =="OnCreate":
            return redirect('addAchievements', profileId =profID,type =type,place=place)
        
        if place =="OnView":
            return redirect('viewPerson', default =type,AtheId =0)
        
        
        
        
def ChooseFederation(request):
    
    if request.method =='GET':
        messages.success(request,"Choose the federation at which your new club belongs")
        
        return render(request, 'manageProfile/ChooseFederation.html')
    
    
def ChooseClub(request):
    
    if request.method =='GET':
       
        return render(request,'manageProfile/ChooseClub.html')
        