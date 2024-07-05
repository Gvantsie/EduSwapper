from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models.interest import Interest
from user.models.skills import Skill
from user.models.user import Profile, User


# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    filter_horizontal = ('skills', 'interests')


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'display_skills', 'display_interests', 'country')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__country', 'profile__skills', 'profile__interests')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'profile__country')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'bio', 'birth_date')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    def display_skills(self, obj):
        return ", ".join([skill.name for skill in obj.profile.skills.all()])
    display_skills.short_description = 'Skills'

    def display_interests(self, obj):
        return ", ".join([interest.name for interest in obj.profile.interests.all()])
    display_interests.short_description = 'Interests'

    def country(self, obj):
        return obj.profile.country
    country.short_description = 'Country'


admin.site.register(User, CustomUserAdmin)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 20


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 20
