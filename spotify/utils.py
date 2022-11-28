from datetime import timedelta
from django.utils import timezone
from requests import post, put, get

from .models import SpotifyToken, Vote
from .credentials import CLIENT_ID, CLIENT_SECRET

AUTH_URL = 'https://accounts.spotify.com'
BASE_API_URL = "https://api.spotify.com/v1/me/"

def establish_session(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    return request.session.session_key

def get_user_tokens(session_id):
    tokens = None
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        tokens = user_tokens[0]
    return tokens

def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    tokens = get_user_tokens(session_id)
    expires_in_time = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.accessToken = access_token
        tokens.refreshToken = refresh_token
        tokens.expiresIn = expires_in_time
        tokens.tokenType = token_type
        tokens.save(update_fields=['accessToken', 'refreshToken', 'expiresIn'])
    else:
        tokens = SpotifyToken(
            user=session_id,
            accessToken=access_token,
            refreshToken=refresh_token,
            tokenType=token_type,
            expiresIn=expires_in_time
        )
        tokens.save()

def is_spotify_authenticated(session_id):
    authenticated = False
    tokens = get_user_tokens(session_id)
    
    if tokens:
        expiry = tokens.expiresIn
        if expiry <= timezone.now():
            refresh_spotify_token(session_id)
        authenticated = True
    return authenticated

def refresh_spotify_token(session_id):
    refresh_token = get_user_tokens(session_id).refreshToken

    response = post(
        f'{AUTH_URL}/api/token',
        data={
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
    ).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')

    update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token)

def execute_spotify_api_request(session_id, endpoint, post_=False, put_=False):
    resp_body = {}
    tokens = get_user_tokens(session_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {tokens.accessToken}'
    }

    # TODO: Catch errors from POST / PUT responses
    if post_:
        resp_body = post(BASE_API_URL + endpoint, headers=headers).json()
        print(resp_body)
    if put_:
        resp_body = put(BASE_API_URL + endpoint, headers=headers).json()
        print(resp_body)

    response = get(BASE_API_URL + endpoint, {}, headers=headers)

    try:
        return response.json()
    except:
        return {'Error': 'Issue with Spotify request'}

def play_song(session_id):
    return execute_spotify_api_request(session_id, 'player/play', put_=True)

def pause_song(session_id):
    return execute_spotify_api_request(session_id, 'player/pause', put_=True)

def skip_song(session_id):
    return execute_spotify_api_request(session_id, 'player/next', post_=True)

def is_valid_song(response):
    if 'error' in response or 'item' not in response:
        return False
    else:
        return True

def create_artist_string(response_item):
    artist_string = ''
    for i, artist in enumerate(response_item.get('artists')):
        if i > 0:
            artist_string += ', '
        name = artist.get('name')
        artist_string += name
    
    return artist_string

def create_song_dict(room, response):
    item = response.get('item')
    song_id = item.get('id')

    votes = Vote.objects.filter(room=room, songId=song_id)

    song_dict = {
            'songId': song_id,
            'title': item.get('name'),
            'artist': create_artist_string(item),
            'duration': item.get('duration_ms'),
            'time': response.get('progress_ms'),
            'imageUrl': item.get('album').get('images')[0].get('url'),
            'isPlaying': response.get('is_playing'),
            'votes': len(votes),
            'votesToSkip': room.votesToSkip
        }

    return song_dict

def get_votes(room_code, song_id=None):
    votes = Vote.objects.filter(room=room_code, songId=song_id)
    return votes
