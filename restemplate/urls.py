from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RatingViewSet, UserSongRatingView, SongStatsView

router = DefaultRouter()

router.register(r'ratings', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
    path('ratings/song/<int:song_id>/user/<int:user_id>/', UserSongRatingView.as_view()),
    path('ratings/song/<int:song_id>/', SongStatsView.as_view()),
]