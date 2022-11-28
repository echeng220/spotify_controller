from django.shortcuts import render, redirect
from requests import Request, post
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


from api.models import Room
from .models import Vote
from api.utils import get_room_by_code
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

from .utils import (
    update_or_create_user_tokens,
    establish_session,
    is_spotify_authenticated,
    execute_spotify_api_request,
    play_song,
    pause_song,
    skip_song,
    is_valid_song,
    create_song_dict,
    get_votes,
    AUTH_URL
)


class AuthURL(APIView):
    def get(self, request, format=None):
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'
        url = Request(
            'GET',
            f'{AUTH_URL}/authorize',
            params={
                'scope': scopes,
                'response_type': 'code',
                'redirect_uri': REDIRECT_URI,
                'client_id': CLIENT_ID,
            }
        ).prepare().url

        return Response({'url': url}, status.HTTP_200_OK)


class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        return Response({'status': is_authenticated}, status.HTTP_200_OK)


def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post(
        f'{AUTH_URL}/api/token',
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    session_key = establish_session(request)
    update_or_create_user_tokens(session_key, access_token, token_type, expires_in, refresh_token)

    return redirect('frontend:')


class CurrentSongView(APIView):
    def get(self, request, format=None):
        room_code = self.request.session.get('room_code')
        room = get_room_by_code(code=room_code)

        if not room:
            return Response({'message': 'You are not in a room!'}, status.HTTP_404_NOT_FOUND)

        host = room.host
        endpoint = 'player/currently-playing'
        response = execute_spotify_api_request(host, endpoint)

        if not is_valid_song(response):
            return Response({'message': 'No song playing!'}, status.HTTP_204_NO_CONTENT)
        
        song_dict = create_song_dict(room, response)

        self.update_room_song(room, song_dict['songId'])
        
        return Response(song_dict, status.HTTP_200_OK)

    def update_room_song(self, room, song_id):
        current_song = room.currentSong

        if current_song != song_id:
            room.currentSong = song_id
            room.save(update_fields=['currentSong'])
            votes = Vote.objects.filter(room=room)


class PlaySongView(APIView):
    def put(self, response, format=None):
        room_code = self.request.session.get('room_code')
        room = get_room_by_code(room_code)

        if self.request.session.session_key == room.host or room.guestCanPause:
            play_song(room.host)
            return Response({}, status.HTTP_204_NO_CONTENT)

        return Response({}, status.HTTP_403_FORBIDDEN)


class PauseSongView(APIView):
    def put(self, response, format=None):
        room_code = self.request.session.get('room_code')
        room = get_room_by_code(room_code)

        if self.request.session.session_key == room.host or room.guestCanPause:
            pause_song(room.host)
            return Response({}, status.HTTP_204_NO_CONTENT)

        return Response({}, status.HTTP_403_FORBIDDEN)


class SkipSongView(APIView):
    def post(self, request, format=None):
        establish_session(request)

        room_code = self.request.session.get('room_code')
        room = get_room_by_code(room_code)

        votes = Vote.objects.filter(room=room, songId=room.currentSong)
        votes_needed = room.votesToSkip

        if self.request.session.session_key == room.host or len(votes) + 1 >= votes_needed:
            votes.delete()
            skip_song(room.host)
        else:
            vote = Vote(
                user=self.request.session.session_key,
                room=room,
                songId=room.currentSong
            )
            vote.save()

        return Response({}, status.HTTP_204_NO_CONTENT)
