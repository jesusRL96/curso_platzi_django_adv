from django.contrib import admin
from cride.circles.models import Circle

@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    """Circle Admin"""
    list_display = ('slug_name', 'verified', 'name', 'is_public')
    search_fields = ('slug_name', 'name',)
    list_filter = ('verified', 'is_public', 'is_limited')