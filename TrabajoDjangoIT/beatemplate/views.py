import os
import requests

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q

from django.core.paginator import Paginator

from taggit.models import Tag
from django_tomselect.autocompletes import AutocompleteModelView

from .models import Artist, Release, Playlist, Song
from .forms import RegisterForm, CreatePlaylistForm, RatingForm

API_URL = os.getenv('API_URL', 'http://web-api:8001/api')
API_CREDS = {'username': os.getenv('API_USER', 'grupo7'), 'password': os.getenv('API_PASSWORD', 'grupo7')}

class SongAutocompleteView(AutocompleteModelView):
    model = Song
    search_lookups = ['song_title__icontains',
                      'artists__artist_name__icontains',
                      'tags__name__icontains']
    ordering = ['song_title']
    page_size = 20

def home(request):
    return render(request, 'beatemplate/home.html')

def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            new_account = register_form.save( commit = False )
            new_account.set_password(register_form.cleaned_data['password'])
            new_account.save()
            login(request, new_account)
            return render(request, 'beatemplate/users/register_completed.html', {'new_account': new_account})
        
    else:
        register_form = RegisterForm()
        
    return render(request, 'beatemplate/users/register.html', {'register_form': register_form})

def feed(request):
    # 1. Paginación de Álbumes (4 por página)
    albumes_lista = Release.objects.get_published_albums()
    paginator_albumes = Paginator(albumes_lista, 4)
    page_albumes = request.GET.get('page_albumes')
    albumes_paginados = paginator_albumes.get_page(page_albumes)

    # 2. Paginación de Singles (4 por página)
    singles_lista = Release.objects.get_published_singles()
    paginator_singles = Paginator(singles_lista, 4)
    page_singles = request.GET.get('page_singles')
    singles_paginados = paginator_singles.get_page(page_singles)

    # 3. Paginación de Lanzamientos Anunciados (4 por página)
    anunciados_lista = Release.objects.get_announced_releases()
    paginator_anunciados = Paginator(anunciados_lista, 4)
    page_anunciados = request.GET.get('page_anunciados')
    anunciados_paginados = paginator_anunciados.get_page(page_anunciados)

    # 4. Paginación de Playlists (4 por página)
    playlists_lista = Playlist.objects.all()
    paginator_playlists = Paginator(playlists_lista, 4)
    page_playlists = request.GET.get('page_playlists')
    playlists_paginadas = paginator_playlists.get_page(page_playlists)

    # 5. Paginación de Artistas (6 por página)
    artistas_lista = Artist.objects.all()
    paginator_artistas = Paginator(artistas_lista, 6) 
    page_artistas = request.GET.get('page_artistas')
    artists_paginados = paginator_artistas.get_page(page_artistas)

    group = {
             'published_albums' : albumes_paginados,
             'published_singles' : singles_paginados,
             'announced_releases' : anunciados_paginados,
             'playlists' : playlists_paginadas,
             'artists' : artists_paginados,
            }

    return render(request, 'beatemplate/feed.html', group)

def detailed_artist(request, id, slug):
    artist = get_object_or_404(Artist, id = id, artist_slug = slug)

    return render(request, 'beatemplate/beats/detailed_artist.html', {'artist' : artist})


def detailed_release(request, id, slug):
    release = get_object_or_404(Release, id = id, release_slug = slug)
    
    return render(request, 'beatemplate/beats/detailed_release.html', {'release' : release})

def detailed_playlist(request, id, slug):
    playlist = get_object_or_404(Playlist, id = id, playlist_slug = slug)
    
    return render(request, 'beatemplate/beats/detailed_playlist.html', {'playlist' : playlist})

def search(request):
    query = request.GET.get('q')
    songs = []
    releases = []
    playlists = []
    artists = []

    if query:
        total = 0
        tag = Tag.objects.filter(slug = query.lower()).first()

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
def new_playlist(request):

    if request.method == "POST":

        form = CreatePlaylistForm( data = request.POST )
        playlist = None

        if form.is_valid():
            playlist = form.save( commit = False )
            playlist.user = request.user
            playlist.save()
            form.save_m2m()

        return redirect(playlist.get_absolute_url())
    else: 
        form = CreatePlaylistForm()

    return render(request, 'beatemplate/beats/new_playlist.html', {'form': form})


def obtain_api_token():
    try:
        resp = requests.post(f"{API_URL}/token/", data=API_CREDS, timeout=2)
        
        if resp.status_code == 200:
            return resp.json()['access']
    
    except requests.RequestException:
        pass

    return None

@login_required
def detailed_song(request, id, slug):
    song = get_object_or_404(Song, id = id, song_slug = slug)
    token = obtain_api_token()
    rating_stats = {'mean_score': 0, 'total_ratings': 0}
    user_rating = None
    rating_form = RatingForm()
    

    if token:
        headers = {'Authorization': f'Bearer {token}'}

        try:
            response = requests.get(f'{API_URL}/ratings/song/{song.id}/', headers = headers)

            if response.status_code == 200:
                rating_stats = response.json()

            else:
                rating_stats = {'mean_score': 0, 'total_ratings': 0}

        except requests.RequestException:
            rating_stats = {'mean_score': 0, 'total_ratings': 0}

        try:
            response = requests.get(f'{API_URL}/ratings/song/{song.id}/user/{request.user.id}/', headers = headers)

            if response.status_code == 200:
                user_rating = response.json()
            
            else:
                user_rating = None
            
        except requests.RequestException:
            user_rating = None

        if request.method == 'POST':
            rating_form = RatingForm(request.POST)

            if rating_form.is_valid():
                payload = {'song': song.id,
                        'user': request.user.id,
                        'score': rating_form.cleaned_data['score']}
                

                if user_rating:
                    rating_id = user_rating.get('id')
                    response = requests.put(f'{API_URL}/ratings/{rating_id}/', json=payload, headers=headers)
                else:
                    response = requests.post(f'{API_URL}/ratings/', json=payload, headers=headers)
                
                if response.status_code in [200, 201]:

                    return redirect(song.get_absolute_url())

        else:
            if user_rating:
                rating_form = RatingForm( initial = {'score': user_rating['score']})

            else:
                rating_form = RatingForm()

    return render(request, 'beatemplate/beats/detailed_song.html', {'song': song,
                                                                    'rating_form': rating_form,
                                                                    'rating_stats': rating_stats,
                                                                    'user_rating' : user_rating})
