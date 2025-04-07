from django.contrib import admin
from .models import CustomUser, Scheme
from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Scheme)

# Register your models here.
