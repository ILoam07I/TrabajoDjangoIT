
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q
from taggit.models import Tag

from .models import Artist, Release, Playlist, Song
from .forms import RegisterForm, CreatePlaylistForm

def home(request):
    return render(request, 'beatemplate/home.html')

def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            new_account = register_form.save(commit=False)
            new_account.set_password(register_form.cleaned_data['password'])
            new_account.save()
            login(request, new_account)
            return render(request, 'beatemplate/register_completed.html', {'new_account': new_account})
        
    else:
        register_form = RegisterForm()
        
    return render(request, 'beatemplate/register.html', {'register_form': register_form})

def feed(request):
    artists = Artist.objects.all()
    published_albums = Release.objects.get_published_albums()
    published_singles = Release.objects.get_published_singles()
    announced_releases = Release.objects.get_announced_releases()
    
    group = {'artists' : artists,
             'published_albums' : published_albums,
             'published_singles' : published_singles,
             'announced_releases' : announced_releases}
    
    return render(request, 'beatemplate/feed.html', group)

def detailed_artist(request, id, slug):
    artist = get_object_or_404(Artist, id = id, artist_slug = slug)
    
    return render(request, 'beatemplate/detailed_artist.html', {'artist' : artist})

def detailed_release(request, id, slug):
    release = get_object_or_404(Release, id = id, release_slug = slug)
    
    return render(request, 'beatemplate/detailed_release.html', {'release' : release})

def detailed_song(request, id, slug):
    song = get_object_or_404(Release, id = id, song_slug = slug)
    
    return render(request, 'beatemplate/detailed_song.html', {'song' : song})

def detailed_playlist(request, id, slug):
    playlist = get_object_or_404(Release, id = id, playlist_slug = slug)
    
    return render(request, 'beatemplate/detailed_playlist.html', {'playlist' : playlist})

def search(request):
    query = request.GET.get('q')
    songs = []
    releases = []
    playlists = []
    artists = []

    if query:
        total = 0
        tag = Tag.objects.filter(slug = query).first()

        if tag:
            return redirect('beatemplate:tag_search', slug = tag.slug)

        else:    
            songs = Song.objects.filter(Q(song_title__icontains = query)).distinct()
            total += songs.count()

            releases = Release.objects.filter(Q(release_title__icontains = query)).distinct()
            total+= releases.count()

            playlists = Playlist.objects.filter(Q(playlist_title__icontains = query))
            total+= playlists.count()

            artists = Artist.objects.filter(Q(artist_name__icontains = query))
            total+= artists.count()
        
            return render(request, 'beatemplate/search/results.html', {'query': query,
                                                                        'songs': songs,
                                                                        'releases': releases,
                                                                        'playlists': playlists,
                                                                        'artists': artists,
                                                                        'total': total})

def tag_search(request, slug):
    total = 0
    tag = get_object_or_404(Tag, slug = slug)

    songs = Song.objects.filter(tags__in = [tag]).distinct()
    total += songs.count()

    releases = Release.objects.filter(release_songs__song__tags__in = [tag],
                                      release_type = Release.ReleaseType.ALBUM).distinct()
    total += releases.count()

    return render(request, 'beatemplate/search/results.html', {'query': tag.name,
                                                               'songs': songs,
                                                               'releases': releases,
                                                               'total': total,
                                                               'tag': tag})


@login_required
def create_playlist(request):
    pass
