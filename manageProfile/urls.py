from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
   path('',views.home, name="home"),
   
   path('ChooseProfile', views.chooseProfile, name="ChooseProfile"),
   path('creatProfile/<id>/<profile>/<parent>',views.creatProfile, name="creatProfile"),
   path('ViewInformation/<id>/<profile>',views.ViewInformation , name="ViewInformation"),
   path('ParentInfo/<id>',views.ParentInfo , name="ParentInfo"),
   path('viewPerson/<default>/<AtheId>', views.viewPerson, name="viewPerson"),
   #
   path('CreateCoach/<id>', views.CreateCoach, name="CreateCoach"),
   
   path('updateCoach/<PersonId>/<CoachId>',views.updateCoach,name="updateCoach"),
   
   path('updateParent/<parentId>',views.updateParent, name="updateParent"),
   path('remove/<profId>/<type>',views.remove,name="remove"),
   path('createOfficial',views.createOfficial,name="createOfficial"),
   path('updateOfficial/<PersonId>',views.updateOfficial, name="updateOfficial"),
   
   path('addAchievements/<profileId>/<type>/<place>',views.addAchievements,name="addAchievements"),
   path('updateAchievement/<id>/<type>/<place>', views.updateAchievement, name="updateAchievement")
   ,path('removeAchievement/<id>/<type>/<place>', views.removeAchievement, name="removeAchievement")
   

   
]
