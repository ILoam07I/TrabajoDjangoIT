from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.contrib.auth.models import User

class Artist(models.Model):
    artist_name = models.CharField( max_length = 256, unique = True )
    artist_slug = models.SlugField( max_length = 256 )

    class Meta:
        ordering = ['-artist_name']
        indexes = [models.Index( fields = ['-artist_name'] )]
        verbose_name = 'Artista'
        verbose_name_plural = 'Artistas'
    
    def __str__(self):
        return self.name


class Release(models.Model):
    class ReleaseType(models.TextChoices):
        ALBUM = "ALBUM", "Álbum"
        SINGLE = "SINGLE", "Single"

    artists = models.ManyToManyField( Artist )
    release_title = models.CharField( max_length = 256 )
    release_slug = models.SlugField( max_length = 256)
    release_date = models.DateField( default = timezone.now )

    @property
    def is_published(self) -> bool:
        return self.release_date <= timezone.now
        
    class Meta:
        ordering = ['-release_date']
        indexes = [models.Index( fields = ['-release_date'] )]
        verbose_name = 'Lanzamiento'
        verbose_name_plural = 'Lanzamientos'
    
    def __str__(self):
        return self.release_title
    

class Song(models.Model):
    artists = models.ManyToManyField( Artist )
    song_title = models.CharField( max_length = 256 )
    song_duartion = models.DurationField()
    song_tags = TaggableManager()

    @property
    def is_playable(self) -> bool:
        today = timezone.now

        return self.song_releases.filter(release__release_date__lte = today).exists()

    class Meta:
        verbose_name = 'Canción'
        verbose_name_plural = 'Canciones'

    def __str__(self):
        return self.song_title


class Disc(models.Model):
    release = models.ForeignKey(Release,
                                on_delete = models.CASCADE,
                                related_name = 'release_discs')
    
    disc_number = models.PositiveIntegerField()
    disc_title = models.CharField( max_length = 256 )

    class Meta:
        ordering = ['disc_number']
        unique_together = ('release', 'disc_number')
        verbose_name = 'Disco'
        verbose_name_plural = 'Discos'
    
    def __str__(self):
        return self.disc_title


class ReleaseSong(models.Model):
    release = models.ForeignKey(Release, 
                                on_delete = models.CASCADE,
                                related_name = 'release_songs')
    
    song = models.ForeignKey(Song,
                             on_delete = models.CASCADE,
                             related_name = 'song_releases')
    
    disc = models.ForeignKey(Disc,
                             null=True,
                             blank=True,
                             on_delete = models.SET_NULL,
                             related_name = 'disc_releases')
    
    track_id = models.PositiveIntegerField()

    class Meta:
        ordering = ['disc__disc_number', 'track_id']
        unique_together = ('release', 'disc', 'track_id')


class Playlist(models.Model):
    user = models.ForeignKey(User,
                             on_delete = models.CASCADE)
    
    playlist_title = models.CharField( max_length = 256 )
    playlist_slug = models.SlugField( max_length = 256 )
    playlist_description = models.CharField( max_length = 256 )
    playlist_date = models.DateField( default = timezone.now )
    playlist_songs = models.ManyToManyField( Song )

    class Meta:
        ordering = ['-playlist_date']
        verbose_name = 'Playlist'
        verbose_name_plural = 'Playlists'

    def __str__(self):
        return self.playlist_title
    