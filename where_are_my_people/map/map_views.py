
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import DatabaseError
from devices.models import Device

class MapView(APIView):
    def get(self, request):
        """
        Handles GET requests to retrieve a list of devices with their latest location and assigned user information.
        Query Parameters:
            device_type (str, optional): Filter devices by device type.
            user_id (int or str, optional): Filter devices by assigned user ID.
        Returns:
            Response: A JSON response containing a list of devices, each with:
                - user: {
                    'id': int,
                    'name': str
                  }
                - device_id: str
                - latitude: float
                - longitude: float
                - timestamp: datetime
            If a database error occurs, returns a 500 error with an error message.
        """
        try:
            devices = Device.objects.filter(assigned_user__isnull=False)
        except DatabaseError as e:
            return Response(
                {"error": "Could not retrieve devices from database"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        device_type = request.query_params.get("device_type")
        user_id = request.query_params.get("user_id")
        print(user_id)
        if device_type:
            devices = devices.filter(device_type=device_type)

        if user_id:
            devices = devices.filter(assigned_user__id=user_id)


        result = []
        for device in devices:
            try:
                location = device.locations.order_by("-ping_time").first()
                if not location:
                    continue

                user = device.assigned_user
                user_name = getattr(user, "name", None) or getattr(user, "username", None) or f"id={user.id}"

                result.append({
                    "user": {
                        "id": user.id,
                        "name": user_name
                    },
                    "device_id": device.device_id,
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "timestamp": location.ping_time
                })
            except Exception as e:
                continue

        return Response(result, status=status.HTTP_200_OK)

