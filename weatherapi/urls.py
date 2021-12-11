from django.urls import include, path
from rest_framework import routers
from .views import (
    ping,
    index,
    WeatherViewSet
)

router = routers.DefaultRouter()
router.register(r'weather-report', WeatherViewSet)


urlpatterns = [
    # path('', index, name='index'),
    path('ping/', ping, name='ping'),
    path('', include(router.urls)),
    # path('management/', include('rest_framework.urls', namespace='rest_framework'))
]
