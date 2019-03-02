import datetime
from django.shortcuts import render
from django.db.models import FieldDoesNotExist, ObjectDoesNotExist
from .models import Location, Weather, Metric
from .serializers import WeatherSerializer, LocationSerializer
from rest_framework import viewsets
from django.http import HttpResponse

# Create your views here.


def ping(request):
    return HttpResponse('pong!')


class WeatherViewSet(viewsets.ModelViewSet):
    """
    API endpoint for fetching the weather data.
    """
    queryset = Weather.objects.all()
    # queryset = WeatherViewSet.get_queryset()
    serializer_class = WeatherSerializer

    def get_queryset(self):

        queryset = Weather.objects.all()

        start_date = self.request.query_params.get('start_date')

        if not start_date:
            start_date = '1901-01-01'

        end_date = self.request.query_params.get('end_date')

        if not end_date:
            end_date = datetime.datetime.today().strftime("%Y-%m-%d")

        metric = self.request.query_params.get('metric')
        if not metric:
            metric = 'TMax'

        location = self.request.query_params.get('location')
        if not location:
            location = 'UK'

        try:
            l = Location.objects.get(name=location)
            m = Metric.objects.get(name=metric)

        except FieldDoesNotExist as e:
            return None

        except ObjectDoesNotExist as e:
            return None

        return queryset.filter(
            metric=m, location=l,
            measured_at__range=[start_date, end_date]
        ).order_by('measured_at')
