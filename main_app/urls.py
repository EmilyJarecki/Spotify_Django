from django.urls import path
from . import views 

urlpatterns = [
    # empty string is localhost
    path('', views.Home.as_view(), name="home"),
    # pay attention that there is no slash before the word
    path('about/', views.About.as_view(), name="about"),
    path('artists/', views.ArtistList.as_view(), name = 'artist_list'),
    path('songs/', views.SongList.as_view(), name='song_list'),
]

