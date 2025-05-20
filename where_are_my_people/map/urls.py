from django.urls import path
from .map_views import MapView

urlpatterns = [
    path('map/', MapView.as_view()),
]   
