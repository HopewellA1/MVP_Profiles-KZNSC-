from django.contrib import admin
from .models import Persons,Nextofkin,Education,Employment,Doctorsinformation

# Register your models here.
admin.site.register(Persons)
admin.site.register(Nextofkin)
admin.site.register(Education)
admin.site.register(Employment)
admin.site.register(Doctorsinformation)