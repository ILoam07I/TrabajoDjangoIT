from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.contrib import admin
from django.urls import reverse
from taggit.models import Tag

class Artist(models.Model):
    artist_name = models.CharField( max_length = 256, unique = True )
    artist_slug = models.SlugField( max_length = 256 )

    class Meta:
        ordering = ['-artist_name']
        indexes = [models.Index( fields = ['-artist_name'] )]
        verbose_name = 'Artista'
        verbose_name_plural = 'Artistas'

    def get_absolute_url(self):
        return reverse( 'beatemplate:detailed_artist', args=[self.id, self.artist_slug] )
    
    def __str__(self):
        return self.artist_name


class ReleaseManager(models.Manager):

    def get_published_albums(self):
        return self.filter(release_date__lte = timezone.now(), release_type = Release.ReleaseType.ALBUM)
    
    def get_published_singles(self):
        return self.filter(release_date__lte = timezone.now(), release_type = Release.ReleaseType.SINGLE)
    
    def get_announced_releases(self):
        return self.filter(release_date__gte = timezone.now())

class Release(models.Model):
    class ReleaseType(models.TextChoices):
        ALBUM = "ALBUM", "Álbum"
        SINGLE = "SINGLE", "Single"

    artists = models.ManyToManyField( Artist )
    release_title = models.CharField( max_length = 256 )
    release_slug = models.SlugField( max_length = 256 )
    release_date = models.DateField( default = timezone.now )
    release_type = models.CharField( max_length=10, choices = ReleaseType.choices, default = ReleaseType.ALBUM)

    objects = ReleaseManager()

    @property
    def is_published(self) -> bool:
        return self.release_date <= timezone.now()
    
    @property
    def get_tags(self):
        tags = set()
        songs = Song.objects.filter( song_releases__release = self )

        for song in songs:
            tags.update( song.tags.all() )
        
        return tags
    
    @admin.display(description = 'Artistas')
    def list_artists(self):
        artists = self.artists.all()
        names = [artist.artist_name for artist in artists]
        
        return ', '.join(names)
        
    class Meta:
        ordering = ['-release_date']
        indexes = [models.Index( fields = ['-release_date'] )]
        verbose_name = 'Lanzamiento'
        verbose_name_plural = 'Lanzamientos'

    def get_absolute_url(self):
        return reverse( 'beatemplate:detailed_release', args=[self.id, self.release_slug] )
    
    def __str__(self):
        return self.release_title
    

class Song(models.Model):
    artists = models.ManyToManyField( Artist )
    song_title = models.CharField( max_length = 256 )
    song_slug = models.SlugField( max_length = 256)
    song_duration = models.DurationField()
    tags = TaggableManager()

    @property
    def is_playable(self) -> bool:
        today = timezone.now()

        return self.song_releases.filter(release__release_date__lte = today).exists()
    
    @admin.display(description = 'Artistas')
    def list_artists(self):
        artists = self.artists.all()
        names = [artist.artist_name for artist in artists]
        
        return ', '.join(names)

    class Meta:
        verbose_name = 'Canción'
        verbose_name_plural = 'Canciones'
    
    def get_absolute_url(self):
        return reverse( 'beatemplate:detailed_song', args=[self.id, self.song_slug] )

    def __str__(self):
        return self.song_title


class ReleaseSong(models.Model):
    release = models.ForeignKey(Release, 
                                on_delete = models.CASCADE,
                                related_name = 'release_songs')
    
    song = models.ForeignKey(Song,
                             on_delete = models.CASCADE,
                             related_name = 'song_releases')
    
    track_number = models.PositiveIntegerField()
    disc_title = models.CharField( max_length = 256, default = None, null = True )

    class Meta:
        verbose_name = 'Canción'
        verbose_name_plural = 'Canciones'
        ordering = ['disc_title', 'track_number']
        unique_together = ('release', 'disc_title', 'track_number')


class Playlist(models.Model):
    user = models.ForeignKey(User,
                             on_delete = models.CASCADE)
    
    playlist_title = models.CharField( max_length = 256 )
    playlist_slug = models.SlugField( max_length = 256 )
    playlist_description = models.CharField( max_length = 256 )
    playlist_date = models.DateTimeField( auto_now_add = True )
    songs = models.ManyToManyField( Song )

    class Meta:
        ordering = ['-playlist_date']
        verbose_name = 'Playlist'
        verbose_name_plural = 'Playlists'
    
    def get_absolute_url(self):
        return reverse( 'beatemplate:detailed_playlist', args=[self.id, self.playlist_slug] )

    def __str__(self):
        return self.playlist_title
    

class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist,
                                 on_delete = models.CASCADE,
                                 related_name = 'playlist_songs')
    
    song = models.ForeignKey(Song,
                             on_delete = models.CASCADE,
                             related_name = 'song_playlists')
    
    position_at = models.PositiveIntegerField()
    added_at = models.DateTimeField( auto_now_add = True )

    class Meta:
        verbose_name = 'Canción'
        verbose_name_plural = 'Canciones'
        ordering = ['position_at']
        unique_together = ('playlist', 'position_at')

    