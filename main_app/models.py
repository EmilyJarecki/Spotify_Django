from django.db import models
import time

# Create your models here.
class Artist(models.Model):

    name = models.CharField(max_length=100)
    img = models.CharField(max_length=250)
    bio = models.TextField(max_length=500)
    verified_artist = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # To display an object in the Django admin site and as the value inserted into a template when it display an object
    def __str__(self):
        return self.name
    # We are ordering by the 'name' field (ascending)
    # https://docs.djangoproject.com/en/4.1/ref/models/options/
    class Meta:
        ordering = ['name']

# below Artist Model

class Song(models.Model):

    title = models.CharField(max_length=150)
    length = models.IntegerField(default=0)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="songs")

    def __str__(self):
        return self.title

    # Here we define the method to look at the length property and convert it
    def get_length(self):
        return time.strftime("%-M:%S", time.gmtime(self.length))