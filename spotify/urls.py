from django.urls import path
from .views import AuthURL, IsAuthenticated, CurrentSongView, PlaySongView, PauseSongView, SkipSongView, spotify_callback

urlpatterns = [
    path('get-auth-url', AuthURL.as_view()),
    path('redirect', spotify_callback),
    path('is-authenticated', IsAuthenticated.as_view()),
    path('current-song', CurrentSongView.as_view()),
    path('play', PlaySongView.as_view()),
    path('pause', PauseSongView.as_view()),
    path('skip', SkipSongView.as_view())
]
