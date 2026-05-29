
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Rating(models.Model):
    song = models.IntegerField()
    user = models.IntegerField()
    score = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(10)])

    class Meta:
        unique_together = ('song', 'user')
        indexes = [models.Index( fields = ['song'] )]
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'
        