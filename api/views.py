from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Room
from .serializers import RoomSerializer, CreateRoomSerializer


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer
    
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guestCanPause')
            votes_to_skip = serializer.data.get('votesToSkip')
            host = self.request.session.session_key

            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guestCanPause = guest_can_pause
                room.votesToSkip = votes_to_skip
                room.save(update_fields=['guestCanPause', 'votesToSkip'])
            else:
                room = Room(host=host, guestCanPause=guest_can_pause, votesToSkip=votes_to_skip)
                room.save()
        
        return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)