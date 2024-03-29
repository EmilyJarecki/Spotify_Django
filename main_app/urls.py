from django.urls import path, include
from . import views

urlpatterns = [
    # '' => localhost:8000
    # views.Home => views.py => class Home
    # name: Helpful for navigation, we can simply say the success url (redirect) is the path named "home"
    path('', views.Home.as_view(), name="home"),
    path('about/', views.About.as_view(), name="about"),
    path('artists/', views.ArtistList.as_view(), name="artist_list"),
    path('songs/', views.SongList.as_view(), name="song_list"),
    # Creating an Artist
    path('artists/new/', views.ArtistCreate.as_view(), name="artist_create"),
    # Show urlpattern
    path('artists/<int:pk>', views.ArtistDetail.as_view(), name="artist_detail"),
    # Update urlpattern
    path('artists/<int:pk>/update',
         views.ArtistUpdate.as_view(), name="artist_update"),
    # Delete urlpattern
    path('artists/<int:pk>/delete',
         views.ArtistDelete.as_view(), name="artist_delete"),
    path('artists/<int:pk>/songs/new/',
         views.SongCreate.as_view(), name="song_create"),
    path('playlists/<int:pk>/songs/<int:song_pk>/',
         views.PlaylistSongAssoc.as_view(), name="playlist_song_assoc"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.Signup.as_view(), name="signup"),
]
