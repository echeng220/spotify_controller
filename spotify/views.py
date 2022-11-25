from django.shortcuts import render, redirect
from requests import Request, post
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


from api.models import Room
from api.utils import get_room_by_code
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

from .utils import (
    update_or_create_user_tokens,
    establish_session,
    is_spotify_authenticated,
    execute_spotify_api_request,
    is_valid_song,
    create_song_dict,
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
        
        song_dict = create_song_dict(response)
        
        return Response(song_dict, status.HTTP_200_OK)
