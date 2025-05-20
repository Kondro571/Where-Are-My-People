from django.urls import path
from .views.location_views import LocationPingView
from .views.devices_views import DevicesView, AssignDeviceView, UnassignDeviceView

urlpatterns = [
    path('devices/', DevicesView.as_view()),
    path('devices/<int:device_id>/unassign/', UnassignDeviceView.as_view()),
    path('devices/<int:device_id>/assign/', AssignDeviceView.as_view()),
    path('devices/<int:device_id>/location/', LocationPingView.as_view()),
]
