from django.contrib import admin
from .models import Member, Court, Schedule, Membership, Announcement

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'phone', 'joined_date')
    search_fields = ('firstname', 'lastname')
    ordering = ('-joined_date',)

@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'notes')
    list_filter = ('status',)
    search_fields = ('name',)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'date', 'time', 'location')
    list_filter = ('type',)
    search_fields = ('title',)
    ordering = ('date', 'time')

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('member', 'type', 'active', 'expiry_date')
    list_filter = ('type', 'active')
    search_fields = ('member__firstname', 'member__lastname')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'important')
    list_filter = ('important',)
    search_fields = ('title',)
    ordering = ('-date_posted',)