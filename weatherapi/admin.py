from django.contrib import admin
from .models import Weather, Location, Metric
# Register your models here.

admin.site.register(Weather)
admin.site.register(Location)
admin.site.register(Metric)