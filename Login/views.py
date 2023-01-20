from datetime import date, datetime
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from Login.models import Register
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordResetForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site 
from .tokens import account_activation_token, Password_Reset_token
from django.core.mail import send_mail, BadHeaderError
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.dateparse import parse_date
from ManagePersonal.models import Persons


def home(request):
    return render(request,'Login/main.html')
# sending email to activate the newly created basic accuount
def ActivationEmail(request, user, to_email):
    mail_subject = "Acivate your account."
    message = render_to_string("Login/ActivationTemplate.html",{
        'user':user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    print(to_email)
    if send_mail(mail_subject,f"{message}"  ,'hopewellsitshaka@gmail.com',[f'{to_email}'], fail_silently=False,
    ):
        return messages.success(request,f"Verification email sent to {to_email}, please verify to access your account.")
    else:
        return messages.error(request, f"There was an erroe sening verification email, please ensure you enter the correct email") 
# registering the user ang adding the additional required informayion
def register(request):
    if request.method == 'GET':
        return render(request,'Login/html screens/register.html')
    else:
        Age = getAge(request.POST['dateOfBirth'])
        if Age >= 18:   
            if request.POST['password1'] == request.POST['password2']:
                try:
                    email= request.POST['email'].lower()
                    
                    #date = parse_date(request.POST["dateOfBirth"]) 
                    user = User.objects.create_user(username =email,password = request.POST['password1'])
                    user.is_active = False           
                    user.save()
                    
                    reg = Register.objects.create(user=user,
                                                
                                                firstName = request.POST['firstName'],
                                                lastName = request.POST['lastName'],
                                                gender = request.POST['inlineRadioOptions'],
                                                dateOfBirth = request.POST['dateOfBirth'],
                                                phoneNumber = request.POST['phoneNumber'],
                                                email= email
                                                )
                    reg.save()
                    try:
                        print(ActivationEmail(request, user, request.POST['email'].lower()))
                    except:
                        messages.error(request,"Could not send email due lack of conection")
                    return redirect('home')
                except IntegrityError:
                    messages.error(request, f"Email Already in use, if it's you can login or reset your password if forgotten")           
                
                    return render(request,'Login/html screens/register.html')
            else:
                messages.error(request,f"Passwords did not match, please try again")           
                
                return render(request,'Login/html screens/register.html')
        else:
            messages.error(request,f"Hello {request.POST['firstName']} are not older than 18, ask your parent to create an account on behalf of you. Thanks, bye")
            return render(request,'Login/html screens/register.html')
                      
def loginuser(request):
    if request.method == 'GET':
        return render(request,'Login/html screens/login.html')  
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        msg = ""
        if user is None:
            try:
                user = User.objects.get(username=request.POST['username'])
                if user:
                    if user.is_active == False:
                        msg="Your account has not been activated please check your emails to find instructions to activate you account"             
            except:
                pass
            
            if msg =="":
                messages.error(request,f"Username or password is wrong please try again. Alternatively create an acoount if you do not have one")           
            else:
                messages.error(request, f"{msg}")
            
            
            return render(request,'Login/html screens/login.html')
        else:
            
            login(request,user)
          
            return redirect('home')
@login_required     
def Account(request):
    
    # here is where the basic account created from the "regiser" action can be viewed and updated
    user = request.user
    RegAccount = Register.objects.get(user = user)
    person =''
    if request.method == 'GET':
        try:
            person = get_object_or_404(Persons,user = user)
        except:
            pass
        return render(request, 'Login/html screens/updateuser.html',{"reg": RegAccount,"person":person} )
    else:
        if request.POST["firstName"]:
            RegAccount.firstName = request.POST["firstName"]
        if request.POST["lastName"]:
            RegAccount.lastName = request.POST["lastName"]
        if request.POST["dateOfBirth"]:
            RegAccount.dateOfBirth = request.POST["dateOfBirth"]
        if request.POST["inlineRadioOptions"]:
            RegAccount.gender = request.POST["inlineRadioOptions"]
        if request.POST["email"]:
            user.email = request.POST["email"].lower()
            user.username = request.POST["email"].lower()
            RegAccount.email = request.POST["email"].lower()
        if request.POST["phoneNumber"]:
            RegAccount.phoneNumber = request.POST["phoneNumber"]
        RegAccount.save()
        user.save()
        messages.success(request,f"Your user account has been successfully updated")           
        try:
            person = get_object_or_404(Persons,user = user)
        except:
            pass 
        return render(request, 'Login/html screens/updateuser.html',{"reg": RegAccount,"person":person} )
            
def activate(request, uidb64, token):
   # This is the action from the activation email that is sent when the use registers the basic account
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        
        user.save()
        reG = Register.objects.get(user=user)
        messages.success(request,f"welcome {reG.firstName} {reG.lastName}, your account has been verified and made active please proceed to login")
       
       
    return redirect('home')  
        
@login_required
def logoutuser(request):
   # if request.method == 'POST':
        logout(request)
        return redirect('home')
    



#sendin the password reset email
def ResetEmail(request, user, to_email):
    print(f"To user: {user.username}")
    mail_subject = "Resert your password."
    message = render_to_string("Login/resertTemplate.html",{
        'user':user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    print(f"to email: {to_email}")
    if send_mail(mail_subject,f"{message} "  ,'hopewellsitshaka@gmail.com',[f'{to_email}'], fail_silently=False,
    ):
        print("Sent")
        return messages.success(request,f"An email is sent to {to_email}, which has the access to resert you password.")
    else:
        return messages.error(request, f"There was an erroe sening verification email, please ensure you enter the correct email")
#page for requesting a link to reset password 
def password_reset_request(request):

    if request.method =='POST':
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            
            data = password_form.cleaned_data['email']
           
            
            user = User.objects.get(username = request.POST['email'].lower())
            print(f"The user is : {user}")
           
            if user:
                print(ResetEmail(request, user, user))
                

            return redirect('password_reset_done')        
    else:
        password_form = PasswordResetForm()
        context = {
        'password_form': password_form,
        }
    return render(request,'Login/password_reset.html', context)  

#Getting The new user's age using the date of Birth
def getAge(Date):
    date = parse_date(Date)
    today = datetime.now()
    year = date.year
    CurrentYear = today.year
    age =CurrentYear - year   
    return age





