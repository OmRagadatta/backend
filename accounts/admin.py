from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')
    search_fields = ('user__username',)
    ordering = ('user',)

admin.site.register(Profile, ProfileAdmin)
