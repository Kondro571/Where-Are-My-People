from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .users_serializer import UserSerializer
from devices.models import Device
from rest_framework import status

class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLastLocationView(APIView):
    def get(self, request, user_id):
        """
        Retrieve the latest location data for a user by their user ID.
        Args:
            request (Request): The HTTP request object.
            user_id (int): The ID of the user whose location is being requested.
        Returns:
            Response: 
                - 200 OK with the latest latitude, longitude, and timestamp if location data is found.
                - 404 NOT FOUND with an error message if the user does not exist, has no assigned device, or no location data is available.
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": f"User with id {user_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        device = Device.objects.filter(assigned_user=user).first()
        if not device:
            return Response({"error": "User has no assigned device"}, status=status.HTTP_404_NOT_FOUND)

        location = device.locations.order_by("-ping_time").first()
        if not location:
            return Response({"error": "No location data available for this device"}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "latitude": location.latitude,
            "longitude": location.longitude,
            "timestamp": location.ping_time
        }, status=status.HTTP_200_OK)