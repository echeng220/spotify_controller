from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Room
from .serializers import RoomSerializer, CreateRoomSerializer


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class GetRoomView(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code:
            room = Room.objects.filter(code=code)
            if room:
                data = RoomSerializer(room[0]).data
                data['isHost'] = self.request.session.session_key == room[0].host
                resp_status = status.HTTP_200_OK
                resp_body = data
            else:
                resp_status = status.HTTP_404_NOT_FOUND
                resp_body = {'Room not found': 'Invalid room code'}
        else:
            resp_status = status.HTTP_400_BAD_REQUEST
            resp_body = {'Bad request': 'Code parameter not found in request'}
        return Response(resp_body, resp_status)

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