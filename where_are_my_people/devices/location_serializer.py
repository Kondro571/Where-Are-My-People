
from rest_framework import serializers

class LocationPingSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    ping_time = serializers.DateTimeField()

    def validate(self, data):
        if not (-90 <= data['latitude'] <= 90):
            raise serializers.ValidationError("Latitude must be between -90 and 90.")
        if not (-180 <= data['longitude'] <= 180):
            raise serializers.ValidationError("Longitude must be between -180 and 180.")
        return data