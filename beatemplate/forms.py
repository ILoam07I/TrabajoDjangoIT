
from django import forms
from django.contrib.auth import get_user_model
from django_tomselect.forms import TomSelectModelMultipleChoiceField
from django_tomselect.app_settings import TomSelectConfig

from .models import Playlist

class CreatePlaylistForm(forms.Form):
    playlist_title = forms.CharField( max_length = 256 )
    playlist_description = forms.CharField( max_length = 256 )

    songs = TomSelectModelMultipleChoiceField(
        config = TomSelectConfig(url = 'beatemplate:autocomplete-song',
                                 value_field = 'id',
                                 label_field = 'song_title',
                                 placeholder = 'Buscar canciones...',
                                 minimum_query_length = 2,
                                 preload = 'focus')
    )

    class Meta:
        model = Playlist
        fields = [ 'playlist_title', 'playlist_description','songs' ]


class RatingForm(forms.Form):
    score = forms.FloatField(label='Puntuación', min_value = 0, max_value = 10)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repetir contraseña', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']
        help_texts = {'username': None}

    def clean_password2(self):
        cd = self.cleaned_data

        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        
        return cd['password2']
