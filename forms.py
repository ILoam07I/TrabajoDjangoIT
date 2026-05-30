from django import forms
from django.contrib.auth import get_user_model
from django_tomselect.forms import TomSelectModelMultipleChoiceField
from django_tomselect.app_settings import TomSelectConfig
from .models import Playlist

class CreatePlaylistForm(forms.ModelForm):
    playlist_title = forms.CharField( 
        max_length=256,
        label='Título de la Playlist',
        widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary mb-3'})
    )
    playlist_description = forms.CharField( 
        max_length=256,
        label='Descripción',
        widget=forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary mb-3', 'rows': 3})
    )

    songs = TomSelectModelMultipleChoiceField(
        config=TomSelectConfig(
            url='beatemplate:autocomplete-song',
            value_field='id',
            label_field='song_title',
            placeholder='Buscar canciones...',
            minimum_query_length=2,
            preload='focus'
        )
    )

    class Meta:
        model = Playlist
        fields = ['playlist_title', 'playlist_description', 'songs']

class RatingForm(forms.Form):
    score = forms.FloatField(
        label='Puntuación', 
        min_value=0, 
        max_value=10,
        widget=forms.NumberInput(attrs={'class': 'form-control bg-dark text-white border-secondary ms-2', 'style': 'max-width: 100px;'})
    )

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control bg-dark text-white border-secondary mb-3'}))
    password2 = forms.CharField(label='Repetir contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control bg-dark text-white border-secondary mb-3'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']
        help_texts = {'username': None}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary mb-3'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary mb-3'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary mb-3'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-dark text-white border-secondary mb-3'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cd['password2']