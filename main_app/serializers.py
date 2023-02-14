# we will be using HyperlinkedModelSerializer because we want to specify model fields we want to include in API

# import base serializer class and model
from rest_framework import serializers
from .models import Artist

# Meta class 
class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    # We are creating a HyperlinkedRelatedField and pointing it to the song_detail view
    songs = serializers.HyperlinkedRelatedField(
        # 'view_name' comes from urls.py path
        view_name='song_detail',
        many=True,
        read_only=True
    )
    class Meta:
       model = Artist
       fields = ('id', 'name', 'img', 'bio', 'verified_artist',)