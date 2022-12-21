from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from .models import Athlete,Persons
from django.utils.dateparse import parse_date
from datetime import date, datetime

def home(request):
    if request.method == 'GET':
        return render(request,'manageProfile/home.html')
    if request.method == 'POST':
        Person = Persons.objects.create(IdentityNumber = request.POST['IdentityNumber'],FirstName = request.POST['FirstName'])
        p = Persons.objects.get(IdentityNumber = Person.IdentityNumber)
        print(p.personId)
        return render(request, 'manageProfile/ChooseProfile.html',{"person": p.personId})

def chooseProfile(request):
    if request.method == 'GET':
        return render(request, 'manageProfile/ChooseProfile.html')
    if request.method == 'POST':

        Person = get_object_or_404(Persons, pk = request.POST['person'])
        return redirect('creatProfile', id=Person.personId, profile="Athlate")
       # return render(request, 'manageProfile/CreateProfile.html',{"person": Person.personId})

def creatProfile(request,id, profile):
    prof =''
    if request.method =="GET":
        try:
            if profile =="Athlate":
                prof = Athlete.objects.get(personId = id)
        except:
            pass

        return render(request, 'manageProfile/CreateProfile.html',{"profile":prof})
    if request.method=='POST':
        print(f"\nRequest\n{request}\n\n")
        print("On the create post")
        #creating athlate instance
        ProfDefault = False
        Person = get_object_or_404(Persons, pk = id)
        if Person.NumProfile == 0:
           ProfDefault = True
        athlete = Athlete.objects.create(personId = Person,
                                        ProfileImage=request.FILES['ProfileImage'],
                                         Federation = request.POST['Federation'],
                                         PlayerType = request.POST['PlayerType'],
                                         AthleteLevel = request.POST['AthleteLevel'],
                                         ClubName = request.POST['ClubName'],
                                         ClubLevel = request.POST['ClubLevel'],
                                         JoinDate = datetime.now(),
                                         Default = ProfDefault
                                         )
        Person.NumProfile += 1
        Person.save()

        print(f"The new athlete object: {athlete}")
        if profile =="Athlate":
                prof = Athlete.objects.get(personId = id)


       # person = Persons.objects.get()
        #athlate = Athlete.objects.create()
        return redirect('ViewInformation', id=Person.personId, profile="Athlate")
       # return render(request, 'manageProfile/CreateProfile.html',{"profile":prof})


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
                
            messages.success(request,f"Dear {Person.FirstName} your profile information has been updated successfully")
            athlete.save()
            return redirect('ViewInformation', id=Person.personId, profile="Athlate")
           
        return render(request, 'manageProfile/ViewInfo.html',{"person":Person, "profile":prof,"type":profile})







