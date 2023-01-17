from django.contrib import admin
from .models import Athlete,Parent,Coach,Official

admin.site.register(Athlete)

admin.site.register(Parent)
admin.site.register(Coach)
admin.site.register(Official)

