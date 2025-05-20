from django.shortcuts import render

from rest_framework.views import APIView
from ..services.device_services import assign_device_to_user
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from ..models import Device

class DevicesView(APIView):
    
    def get(self, request):
        """
        Handles GET requests to retrieve a list of all devices.
        For each device, returns:
            - device_id: The unique identifier of the device.
            - assigned: Boolean indicating if the device is assigned to a user.
            - user: If assigned, an object containing the user's id and name (or username if name is not available); otherwise, None.
        Returns:
            Response: A DRF Response object containing a list of device information with HTTP 200 OK status.
        """
        devices = Device.objects.all()
        result = []

        for device in devices:
            assigned_user = device.assigned_user
            result.append({
                "device_id": device.device_id,
                "assigned": bool(assigned_user),
                "user": {
                    "id": assigned_user.id,
                    "name": getattr(assigned_user, "name", assigned_user.username)
                } if assigned_user else None
            })

        return Response(result, status=status.HTTP_200_OK)
    
class AssignDeviceView(APIView):
    def post(self, request, device_id):
        """
        Assigns a device to a user.
        Handles POST requests to assign a device (specified by `device_id`) to a user (specified by `user_id` in the request data).
        Returns a success response if the assignment is successful.
        Returns a 400 Bad Request if `user_id` is missing or invalid.
        Returns a 404 Not Found if the device or user does not exist.
        Args:
            request: The HTTP request object containing the data.
            device_id: The ID of the device to be assigned.
        Returns:
            Response: A DRF Response object with the assignment status or error message.
        """
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            assign_device_to_user(device_id, user_id)
            return Response({"status": "assigned"}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UnassignDeviceView(APIView):
    def post(self, request, device_id):
        """
        Unassigns a user from the specified device.
        Args:
            request (Request): The HTTP request object.
            device_id (int): The ID of the device to unassign.
        Returns:
            Response: 
                - 200 OK with {"status": "unassigned"} if the device was successfully unassigned.
                - 200 OK with {"message": "Device is already unassigned"} if the device had no assigned user.
                - 404 Not Found with {"error": "Device not found"} if the device does not exist.
        """
        try:
            device = Device.objects.get(id=device_id)
        except Device.DoesNotExist:
            return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

        if not device.assigned_user:
            return Response({"message": "Device is already unassigned"}, status=status.HTTP_200_OK)

        device.assigned_user = None
        device.save()
        return Response({"status": "unassigned"}, status=status.HTTP_200_OK)
    
    
