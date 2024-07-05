from django.contrib import admin
from .models import Match


# Register your models here.
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'is_accepted_by_user1', 'is_accepted_by_user2')
    list_filter = ('is_accepted_by_user1', 'is_accepted_by_user2')
    search_fields = ('user1__username', 'user2__username')
    fieldsets = (
        (None, {
            'fields': ('user1', 'user2')
        }),
        ('Acceptance', {
            'fields': ('is_accepted_by_user1', 'is_accepted_by_user2')
        }),
    )
