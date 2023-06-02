from django.shortcuts import redirect
# view class handles requests
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
# a class to handle sending a type of response
from django.http import HttpResponse
from django.urls import reverse
from .models import Artist, Playlist
from .models import Song as SingleSong
# user authorization
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
# user authentication
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class Song:
    def __init__(self, song_name, artist):
        self.song_name = song_name
        self.artist = artist

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

# this line protects route for user auth
# if you try to navigate to /artists it will redirect you to /login
@method_decorator(login_required, name='dispatch')
class ArtistList(TemplateView):

    # anticipated artist_list has yet to be created (our next step)
    template_name = "artist_list.html"

    # kwargs allows use to pass a variable number of keyword arguments to a Python function
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # this is to get the query parameter. We have to access it in the request.GET dictionary object
        name = self.request.GET.get("name")
        if name != None:

            # use .filter (user=self.request.user) because of user auth so that the list is only theirs
            context['artists'] = Artist.objects.filter(
                name__icontains=name, user=self.request.user)
            context['header'] = f'Searching for {name}'
        else:

            # using the model to query the database
            context['artists'] = Artist.objects.filter(user=self.request.user)
            context['header'] = 'Trending Artists'
        return context

@method_decorator(login_required, name='dispatch')
class ArtistCreate(CreateView):
    model = Artist
    fields = ['name', 'img', 'bio', 'verified_artist']
    template_name = "artist_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ArtistCreate, self).form_valid(form)
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

@method_decorator(login_required, name='dispatch')
class ArtistDelete(DeleteView):
    model = Artist
    template_name = 'artist_delete_confirmation.html'
    success_url = '/artists/'

@method_decorator(login_required, name='dispatch')
class SongList(TemplateView):
    template_name = 'song_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['songs'] = songs
        return context
        
@method_decorator(login_required, name='dispatch')
class SongCreate(View):
    def post(self, request, pk):
        title = request.POST.get("title")
        length = request.POST.get("length")
        artist = Artist.objects.get(pk=pk)
        SingleSong.objects.create(title=title, length=length, artist=artist)
        return redirect('artist_detail', pk=pk)

@method_decorator(login_required, name='dispatch')
class Home(TemplateView):
    template_name = "home.html"
    # Here we have added the playlists as context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["playlists"] = Playlist.objects.all()
        return context

@method_decorator(login_required, name='dispatch')
class PlaylistSongAssoc(View):
    def get(self, request, pk, song_pk):
        # get the query param from the url
        assoc = request.GET.get("assoc")
        if assoc == "remove":

            # get the playlist by the id and
            # remove from the join table the given song_id
            Playlist.objects.get(pk=pk).songs.remove(song_pk)
        if assoc == "add":
            
            # get the playlist by the id and
            # add to the join table the given song_id
            Playlist.objects.get(pk=pk).songs.add(song_pk)
        return redirect('home')


@method_decorator(login_required, name='dispatch')

# login is required to view Artist
# DetailView is a generic view provided by Django
class ArtistDetail(DetailView):

    # the model which we will be using
    model = Artist

    # the html file this information will be going into
    template_name = "artist_detail.html"

    # getting extra info into template like allowing the Playlist data to also be accessed
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["playlists"] = Playlist.objects.all()
        return context

# route for signup
class Signup(View):

    # show a form to fill out
    def get(self, request):

        # UserCreationForm() is provided by Django
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)
    
    # on form submit, validate the form and login the user.
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("artist_list")
        else:
            context = {"form": form}
            return render(request, "registration/signup.html", context)
