# # we will be using HyperlinkedModelSerializer because we want to specify model fields we want to include in API

# # import base serializer class and model
# from rest_framework import serializers
# from .models import Artist, Song

# # Meta class 
# class ArtistSerializer(serializers.HyperlinkedModelSerializer):
#     # We are creating a HyperlinkedRelatedField and pointing it to the song_detail view
#     songs = serializers.HyperlinkedRelatedField(
#         # 'view_name' comes from urls.py path
#         view_name='song_detail',
#         many=True,
#         read_only=True
#     )
#     # so that Artist and Song in List view contain a link to their details
#     artist_url = serializers.ModelSerializer.serializer_url_field(
#         view_name='artist_detail'
#     )
#     class Meta:
#        model = Artist
#        fields = ('id', 'name', 'img', 'bio', 'verified_artist')

# class SongSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Song
#         fields = ('pk', 'title', 'length', 'artist')