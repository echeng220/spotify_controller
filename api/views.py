from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Room
from .serializers import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer
from .utils import get_room_by_code, get_room_by_host_id

class BaseView(APIView):
    def establish_session(self, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class GetRoomView(BaseView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        self.establish_session()

        code = request.GET.get(self.lookup_url_kwarg)
        if code:
            room = get_room_by_code(code=code)
            if room:
                data = RoomSerializer(room).data
                data['isHost'] = self.request.session.session_key == room.host
                resp_status = status.HTTP_200_OK
                resp_body = data
            else:
                resp_status = status.HTTP_404_NOT_FOUND
                resp_body = {'Room not found': 'Invalid room code'}
        else:
            resp_status = status.HTTP_400_BAD_REQUEST
            resp_body = {'Bad request': 'Code parameter not found in request'}
        return Response(resp_body, resp_status)

class CreateRoomView(BaseView):
    serializer_class = CreateRoomSerializer
    
    def post(self, request, format=None):
        self.establish_session()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guestCanPause')
            votes_to_skip = serializer.data.get('votesToSkip')
            host_id = self.request.session.session_key

            room = get_room_by_host_id(host_id=host_id)
            if room:
                room.guestCanPause = guest_can_pause
                room.votesToSkip = votes_to_skip
                room.save(update_fields=['guestCanPause', 'votesToSkip'])
            else:
                room = Room(host=host_id, guestCanPause=guest_can_pause, votesToSkip=votes_to_skip)
                room.save()

            self.request.session['room_code'] = room.code
        
        return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)


class JoinRoomView(BaseView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'

    def post(self, request, format=None):
        self.establish_session()

        code = request.data.get(self.lookup_url_kwarg)
        if code:
            room = get_room_by_code(code=code)
            if room:
                self.request.session['room_code'] = code
                resp_body = {'message': 'Room joined!'}
                status_code = status.HTTP_200_OK
            else:
                resp_body = {'message': 'Invalid room code'}
                status_code = status.HTTP_404_NOT_FOUND
        else:
            resp_body = {'message': 'Invalid post data, did not find code key'}
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(resp_body, status_code)


class UserInRoom(BaseView):
    def get(self, request, format=None):
        self.establish_session()

        data = {
            'code': self.request.session.get('room_code')
        }
        return JsonResponse(data, status=status.HTTP_200_OK)


class LeaveRoom(BaseView):
    def post(self, request, format=None):
        msg = 'did nothing'
        
        if 'room_code' in self.request.session:
            room_code = self.request.session.pop('room_code')

            host_id = self.request.session.session_key
            room = get_room_by_host_id(host_id=host_id)

            if room:
                room.delete()
                msg = f'deleted room {room_code}'

        return Response({'message': msg}, status=status.HTTP_200_OK)


class UpdateRoomView(BaseView):
    serializer_class = UpdateRoomSerializer

    def patch(self, request, format=None):
        self.establish_session()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guestCanPause')
            votes_to_skip = serializer.data.get('votesToSkip')
            code = serializer.data.get('code')

            room = get_room_by_code(code=code)
            if not room:
                return Response({'message': 'Room not found'}, status.HTTP_404_NOT_FOUND)

            user_id = self.request.session.session_key

            if room.host != user_id:
                return Response({'message': 'You are not the host of this room'}, status.HTTP_403_FORBIDDEN)

            room.guestCanPause = guest_can_pause
            room.votesToSkip = votes_to_skip
            room.save(update_fields=['guestCanPause', 'votesToSkip'])
            return Response(RoomSerializer(room).data, status.HTTP_200_OK)
        
        return Response({'message': 'Invalid data'}, status.HTTP_400_BAD_REQUEST)
