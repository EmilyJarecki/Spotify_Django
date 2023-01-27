from django.shortcuts import render
# view class handles requests
# from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
# a class to handle sending a type of response
from django.http import HttpResponse
from django.urls import reverse
from .models import Artist


#Instatntiate an artist for our fake database
# no need for it bc it is fake
# class Artist:
#     def __init__(self, name, image, bio):
#         self.name = name
#         self.image = image
#         self.bio = bio

class Song:
    def __init__(self, song_name, artist):
        self.song_name = song_name
        self.artist = artist

# artists = [
#   Artist("Gorillaz", "https://i.scdn.co/image/ab67616d00001e0295cf976d9ab7320469a00a29",
#           "Gorillaz are once again disrupting the paradigm and breaking convention in their round the back door fashion with Song Machine, the newest concept from one of the most inventive bands around."),
#   Artist("Panic! At The Disco",
#           "https://i.scdn.co/image/58518a04cdd1f20a24cf0545838f3a7b775f8080", "Welcome 👋 The Amazing Beebo was working on a new bio but now he's too busy taking over the world."),
#   Artist("Joji", "https://i.scdn.co/image/7bc3bb57c6977b18d8afe7d02adaeed4c31810df",
#           "Joji is one of the most enthralling artists of the digital age. New album Nectar arrives as an eagerly anticipated follow-up to Joji's RIAA Gold-certified first full-length album BALLADS 1, which topped the Billboard R&B / Hip-Hop Charts and has amassed 3.6B+ streams to date."),
#   Artist("Metallica",
#           "https://i.ebayimg.com/images/g/MZAAAOSwjNdb7H-5/s-l500.jpg", "Metallica formed in 1981 by drummer Lars Ulrich and guitarist and vocalist James Hetfield and has become one of the most influential and commercially successful rock bands in history, having sold 110 million albums worldwide while playing to millions of fans on literally all seven continents."),
#   Artist("Bad Bunny",
#           "https://pyxis.nymag.com/v1/imgs/575/9f8/04c0d3bc3381bd54f7cfe181ba562e8280-01-bad-bunny-1.rsquare.w700.jpg", "Benito Antonio Martínez Ocasio, known by his stage name Bad Bunny, is a Puerto Rican rapper, singer, and songwriter. His music is often defined as Latin trap and reggaeton, but he has incorporated various other genres into his music, including rock, bachata, and soul"),
#   Artist("Kaskade",
#           "https://i1.sndcdn.com/artworks-sNjd3toBZYCG-0-t500x500.jpg", "Ryan Gary Raddon, better known by his stage name Kaskade, is an American DJ, record producer, and remixer."),
# ]

songs = [
    Song("Feel Good Inc", "Gorillaz"),
    Song("DARE", "Gorillaz"),
    Song("Sanctuary", "Joji"),
    Song("Ew", "Joji"),
    Song("Fade To Black", "Metallica"),
    Song("Enter Sandman", "Metallica"),
]


# Create your views here.
class Home(TemplateView):
    template_name = "home.html"

class About(TemplateView):
    template_name = "about.html"

class ArtistList(TemplateView):
    # anticipated artist_list has yet to be created (our next step)
    template_name = "artist_list.html"

    # kwargs allows use to pass a variable number of keyword arguments to a Python function 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # this is to get the query parameter. We have to access it in the request.GET dictionary object
        name = self.request.GET.get("name")
        if name != None: 
            # can be "album__icontains=album" if you would like to look it up by album instead of name
            context['artists'] = Artist.objects.filter(name__icontains=name)
            context['header'] = f'Searching for {name}'
        else:
            # .filter is the sql WHERE statement and name__icontains is doing a search for any name that contains the query param

        # Context dictionary should have an artists key which has the value of all instantiated artists from above
        
        #below if for static data/fake database
        # context['artists'] = artists

        #using the model to query the database
            context['artists'] = Artist.objects.all()
            context['header'] = 'Trending Artists'
        return context

class ArtistCreate(CreateView):
    model = Artist
    fields = ['name', 'img', 'bio', 'verified_artist']
    template_name = "artist_create.html"
    # success_url = "/artists/"
    def get_success_url(self):
        return reverse('artist_detail', kwargs={'pk': self.object.pk})

class ArtistDetail(DetailView):
    model = Artist
    template_name = "artist_detail.html"

class ArtistUpdate(UpdateView):
    model = Artist
    fields = ['name', 'img', 'bio', 'verified_artist']
    template_name = 'artist_update.html'
    # success_url = '/artists'
    def get_success_url(self):
        return reverse('artist_detail', kwargs={'pk': self.object.pk})

class ArtistDelete(DeleteView):
    model = Artist
    template_name = 'artist_delete_confirmation.html'
    success_url = '/artists/'

class SongList(TemplateView):
    template_name = 'song_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['songs'] = songs
        return context

