from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
   path('',views.home, name="home"),
   path('personal/<id>',views.personal, name="personal"),
   path('ChooseProfile', views.chooseProfile, name="ChooseProfile"),
   path('creatProfile/<id>/<profile>/<parent>',views.creatProfile, name="creatProfile"),
   path('ViewInformation/<id>/<profile>',views.ViewInformation , name="ViewInformation"),
   path('ParentInfo/<id>',views.ParentInfo , name="ParentInfo")
   
]
