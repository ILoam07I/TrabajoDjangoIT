from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg
from rest_framework import viewsets

from .models import Rating
from .serializers import RatingSerializer


class RatingViewSet(viewsets.ModelViewSet):

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    @action(detail=False, methods=['get'])
    def resumen(self, request):
        song_id = request.query_params.get('song')
        
        if not song_id:
            return Response({"error": "Debes proporcionar un song"}, status=400)

        datos = Rating.objects.filter(song=song_id).aggregate(
            total=Count('id'),
            media=Avg('score')
        )

        return Response({
            "song_id": int(song_id),
            "total_ratings": datos['total'] or 0,
            "mean_score": round(datos['media'] or 0, 1)
        })