
from ..models import Device
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

def assign_device_to_user(device_id, user_id):
    
    try:
        device = Device.objects.get(id=device_id)
    except Device.DoesNotExist:
        raise ObjectDoesNotExist(f"Device with id {device_id} does not exist")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise ObjectDoesNotExist(f"User with id {user_id} does not exist")

    if device.assigned_user and device.assigned_user != user:
        device.assigned_user = None

    existing_device = Device.objects.filter(assigned_user=user).exclude(id=device.id).first()
    if existing_device:
        raise ValueError("User already has a device assigned")

    device.assigned_user = user
    device.save()
