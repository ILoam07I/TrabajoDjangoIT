
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Rating
from .serializers import RatingSerializer, SongRatingSerializer, UserSongRatingSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def resumen(self, request):
        song_id = request.query_params.get('song')
        
        if not song_id:
            return Response({'error': 'Debes proporcionar una canción'}, status = 400)

        datos = Rating.objects.filter(song=song_id).aggregate(total = Count('id'),
                                                              media = Avg('score'))

        return Response({'song_id': int(song_id),
                         'total_ratings': datos['total'] or 0,
                         'mean_score': round(datos['media'] or 0, 1)})
    

class RatingView(APIView):

    def post(self, request):
        song = request.data.get('song')
        user = request.data.get('user')
        score = request.data.get('score')

        rating, created = Rating.objects.update_or_create(song = song,
                                                          user_id = user,
                                                          defaults = {'score': score})

        serializer = RatingSerializer(rating)

        return Response(serializer.data, status = status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class SongStatsView(APIView):

    def get(self, request, song_id):
        stats = Rating.objects.filter(song = song_id).aggregate(total_ratings = Count('id'),
                                                                mean_score = Avg('score'))

        data = {'song_id': song_id,
                'total_ratings': stats['total_ratings'],
                'mean_score': stats['mean_score'] or 0}

        serializer = SongRatingSerializer(data)

        return Response(serializer.data)
    

class UserSongRatingView(APIView):

    def get(self, request, song_id, user_id):
        rating = get_object_or_404(Rating, song=song_id, user=user_id)

        data = {'song_id': rating.song,
                'user_id': rating.user,
                'score': rating.score}

        serializer = UserSongRatingSerializer(data)

        return Response(serializer.data)
    