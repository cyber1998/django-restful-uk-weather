from django.urls import include, path
from rest_framework import routers
from .views import (
    ping,
    WeatherViewSet
)

router = routers.DefaultRouter()
router.register(r'weather-report', WeatherViewSet)


urlpatterns = [
    path('ping/', ping, name='ping'),
    path('', include(router.urls)),
    path('working', include('rest_framework.urls', namespace='rest_framework'))
]
