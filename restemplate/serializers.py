from .models import Rating
from rest_framework import serializers

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class SongRatingSerializer(serializers.Serializer):
    song_id = serializers.IntegerField()
    total_ratings = serializers.IntegerField()
    mean_score = serializers.FloatField()