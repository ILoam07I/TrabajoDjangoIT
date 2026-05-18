
from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'beatemplate'

urlpatterns = [
    path('account/', include('django.contrib.auth.urls')),
    path('', views.home, name = 'home'),
    path('feed/', views.feed, name = 'feed'),
    path('release/<int:id>/<slug:slug>/', views.detailed_release, name = 'detailed_release'),
    path('artist/<int:id>/<slug:slug>/', views.detailed_artist, name = 'detailed_artist'),
    path('song/<int:id>/<slug:slug>/', views.detailed_song, name = 'detailed_song'),
    path('playlist/<int:id>/<slug:slug>/', views.detailed_playlist, name = 'detailed_playlist'),
    path('playlist/create/', views.create_playlist, name = 'create_playlist'),
    path('search/', views.search, name = 'search'),
    path('tag/<slug:slug>/', views.tag_search, name = 'tag_search'), 
    path('register/', views.register, name = 'register'),
]