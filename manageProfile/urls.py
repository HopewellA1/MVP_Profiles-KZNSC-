from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
   path('',views.home, name="home"),
   path('ChooseProfile', views.chooseProfile, name="ChooseProfile"),
   path('creatProfile/<id>/<profile>',views.creatProfile, name="creatProfile"),
   path('ViewInformation/<id>/<profile>',views.ViewInformation, name="ViewInformation")
]
