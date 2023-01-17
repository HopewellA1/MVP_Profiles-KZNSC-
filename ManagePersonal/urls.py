from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
path('personal/<id>',views.personal, name="personal"),
path('updatePersonal<personId>', views.updatePersonal , name="updatePersonal"),
path('addNextOfKin/<PersonId>',views.addNextOfKin, name="addNextOfKin"),
path('updateNextOfKin/<kinId>/<place>', views.updateNextOfKin, name="updateNextOfKin"),

path('AddEducation/<personId>',views.AddEducation, name="AddEducation"),
path('updateEducation/<educationId>/<place>',views.updateEducation,name="updateEducation"),

path('removEducation/<educationId>/<place>',views.removEducation, name ="removEducation"),
path('addEmployment/<personId>', views.addEmployment, name="addEmployment"),
path('updateEmployment/<employmentId>/<place>', views.updateEmployment, name="updateEmployment"),
path('removeEmployment/<employmentId>/<place>', views.removeEmployment, name="removeEmployment"),

path('addDoctor/<personId>', views.addDoctor, name="addDoctor"),
path('updateDoctor/<docId>/<place>',views.updateDoctor, name="updateDoctor"),
path('ToChoose/<id>',views.ToChoose, name="ToChoose")


]
