from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Scheme)

# Register your models here.
admin.site.register(District)
admin.site.register(Taluka)
admin.site.register(GramPanchayat)
admin.site.register(WorkType)
admin.site.register(WorkSuggestion)
