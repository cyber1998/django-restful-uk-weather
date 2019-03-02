from .models import Location, Weather
from rest_framework import serializers


class WeatherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Weather
        fields = ('value', 'measured_at')

    def to_representation(self, obj):
        return {
            str(obj.measured_at.strftime("%Y-%m")): obj.value
                }
        # fields = ('value', 'year', 'month')


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ('name')
