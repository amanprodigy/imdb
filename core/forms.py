from django import forms
from django.contrib.auth import get_user_model

from .models import Vote, Movie


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ('vote', 'user', 'movie')

    user = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=get_user_model().objects.all(),
        disabled=True
    )
    movie = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=Movie.objects.all(),
        disabled=True
    )
    vote = forms.ChoiceField(
        label='Vote',
        widget=forms.RadioSelect,
        choices=Vote.VOTE_CHOICES
    )
