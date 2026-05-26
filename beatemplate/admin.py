from django.contrib import admin

from .models import Artist, Release, Playlist, Song, ReleaseSong, PlaylistSong

class ReleaseSongInline(admin.TabularInline):
    model = ReleaseSong
    fields = ['song', 'track_number', 'disc_title']
    autocomplete_fields = ['song']
    extra = 1
    min_num = 1

class PlaylistSongInline(admin.TabularInline):
    model = PlaylistSong
    fields = ['song', 'position_at']
    autocomplete_fields = ['song']
    extra = 1

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['artist_name', 'artist_slug']
    list_filter = ['artist_name']
    search_fields = ['artist_name']
    prepopulated_fields = {'artist_slug': ('artist_name',)}
    ordering = ['artist_name']
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['list_artists', 'song_title', 'song_slug', 'song_duration']
    list_filter = ['artists', 'song_title']
    autocomplete_fields = ['artists']
    search_fields = ['artists__artist_name', 'song_title', 'tags__name']
    prepopulated_fields = {'song_slug': ('song_title',)}
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    inlines = [ReleaseSongInline]
    list_display = ['list_artists', 'release_title', 'release_slug', 'release_date', 'release_type']
    list_filter = ['artists', 'release_title', 'release_date', 'release_type']
    autocomplete_fields = ['artists']
    search_fields = ['artists__artist_name', 'release_title']
    prepopulated_fields = {'release_slug': ('release_title',)}
    ordering = ['release_date']
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    inlines = [PlaylistSongInline]
    list_display = ['playlist_title', 'playlist_slug', 'playlist_description']
    list_filter = ['playlist_title']
    autocomplete_fields = ['songs']
    search_fields = ['playlist_title']
    prepopulated_fields = {'playlist_slug': ('playlist_title',)}
    ordering = ['playlist_title', 'playlist_date']
    show_facets = admin.ShowFacets.ALWAYS
    