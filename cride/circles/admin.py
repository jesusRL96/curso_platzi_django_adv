from django.contrib import admin
from cride.circles.models import Circle, Membership
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import HttpResponse

from cride.rides.models import Ride
import csv

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

    def download_todays_rides(self, request, queryset):
        now = timezone.now()
        start = datetime(now.year, now.month, now.day,0,0,0)
        end = start + timedelta(days=1)
        rides = Ride.objects.filter(offered_in__in=queryset.values_list('id'), departure_date__range=[start, end])
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filname="somefilename.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'id',
            'passengers',
            'departure_location',
            'departure_date',
            'arrival_location',
            'arrival_date'
            'rating'
            ])
        for ride in rides:
            writer.writerow([
                ride.pk,
                ride.passengers.count(),
                ride.departure_location,
                str(ride.departure_date),
                ride.arrival_location,
                str(ride.arrival_date),
                ride.rating
                ])
        return response
    actions = ['make_verified', 'make_unverified', 'download_todays_rides']

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    """Membership Admin"""