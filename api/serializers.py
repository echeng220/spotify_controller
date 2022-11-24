'''
Translates classes into JSON responses. Create one serializer to handle each request / response.
'''

from rest_framework import serializers

from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    """Serialize a response"""
    class Meta:
        model = Room
        fields = ('id', 'code', 'host', 'guestCanPause', 'votesToSkip', 'createdAt')


class CreateRoomSerializer(serializers.ModelSerializer):
    """Serialize a request"""
    class Meta:
        model = Room
        fields = ('guestCanPause', 'votesToSkip')


class UpdateRoomSerializer(serializers.ModelSerializer):
    # Need to allow for non-unique codes (we aren't creating a new room, we are updating an existing room)
    code = serializers.CharField(validators=[])
    class Meta:
        model = Room
        fields = ('guestCanPause', 'votesToSkip', 'code')
