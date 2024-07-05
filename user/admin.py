from django.contrib import admin

from user.models.interest import Interest
from user.models.skills import Skill
from user.models.user import Profile


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'skills', 'interests', 'country',)
    list_filter = ('user', 'skills', 'interests', 'country',)
    search_fields = ('user', 'skills', 'interests', 'country',)
    list_per_page = 20


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('skill_name',)
    list_filter = ('skill_name',)
    search_fields = ('skill_name',)
    list_per_page = 20


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('interest_name',)
    list_filter = ('interest_name',)
    search_fields = ('interest_name',)
    list_per_page = 20
