
from django.contrib import admin
from django.urls import path, include

from . import views
from .views import SongAutocompleteView

app_name = 'beatemplate'

urlpatterns = [
    path('account/', include('django.contrib.auth.urls')),
    path('', views.home, name = 'home'),
    path('feed/', views.feed, name = 'feed'),
    path('release/<int:id>/<slug:slug>/', views.detailed_release, name = 'detailed_release'),
    path('artist/<int:id>/<slug:slug>/', views.detailed_artist, name = 'detailed_artist'),
    path('song/<int:id>/<slug:slug>/', views.detailed_song, name = 'detailed_song'),
    path('playlist/<int:id>/<slug:slug>/', views.detailed_playlist, name = 'detailed_playlist'),
    path('playlist/create/', views.new_playlist, name = 'new_playlist'),
    path('search/', views.search, name = 'search'),
    path('tag/<slug:slug>/', views.tag_search, name = 'tag_search'), 
    path('register/', views.register, name = 'register'),
    path('autocomplete/song/', SongAutocompleteView.as_view(), name = 'autocomplete-song')
]