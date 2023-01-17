from django.contrib import admin
from .models import Athlete,Parent,Coach,Official,Achievement

admin.site.register(Athlete)

admin.site.register(Parent)
admin.site.register(Coach)
admin.site.register(Official)
admin.site.register(Achievement)

