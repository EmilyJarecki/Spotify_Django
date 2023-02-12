from django.contrib import admin
from .models import Artist, Song, Playlist

# Register your models here.
admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(Playlist)