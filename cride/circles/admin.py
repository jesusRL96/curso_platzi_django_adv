from django.contrib import admin
from cride.circles.models import Circle, Membership

@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    """Circle Admin"""
    list_display = ('slug_name', 'verified', 'name', 'is_public')
    search_fields = ('slug_name', 'name',)
    list_filter = ('verified', 'is_public', 'is_limited')

    def make_verified(self, request, queryset):
        queryset.update(verified=True)
    make_verified.short_description = 'Make selected circles verified'

    def make_unverified(self, request, queryset):
        queryset.update(verified=False)
    make_unverified.short_description = 'Make selected circles unverified'

    actions = ['make_verified', 'make_unverified']

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    """Membership Admin"""