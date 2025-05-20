
from ..models import Device
from ..models import Location
from django.core.exceptions import ObjectDoesNotExist

def save_location_ping(device_id, data):
    try:
        device = Device.objects.get(id=device_id)
    except Device.DoesNotExist:
        raise ObjectDoesNotExist(f"Device with id {device_id} does not exist")

    if not device.assigned_user:
        raise ValueError("Device is not assigned to any user")

    Location.objects.create(device=device, **data)
