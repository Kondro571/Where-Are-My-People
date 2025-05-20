from rest_framework.views import APIView
from ..services.location_services import save_location_ping
from rest_framework.response import Response
from ..location_serializer import LocationPingSerializer
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

class LocationPingView(APIView):
    def post(self, request, device_id):
        """
        Handles POST requests to create a new location ping for a given device.

        Args:
            request (Request): The HTTP request object containing the location data.
            device_id (int or str): The unique identifier of the device for which the location ping is being recorded.

        Returns:
            Response: 
                - 200 OK with {"status": "ok"} if the location ping is saved successfully.
                - 404 NOT FOUND with {"error": "..."} if the device does not exist.
                - 400 BAD REQUEST with {"error": "..."} if there is a value error or serializer validation fails.
                - 400 BAD REQUEST with serializer errors if the input data is invalid.
        """
        serializer = LocationPingSerializer(data=request.data)
        if serializer.is_valid():
            try:
                save_location_ping(device_id, serializer.validated_data)
                return Response({"status": "ok"})
            except ObjectDoesNotExist as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)