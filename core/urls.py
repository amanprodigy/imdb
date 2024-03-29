from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('movies/<int:pk>/', views.MovieDetail.as_view(), name='movie-detail'),
    path('movies/', views.MovieList.as_view(), name='movie-list'),
    path('movie/<int:movie_id>/vote/', views.CreateVote.as_view(),
         name='create-vote'),
    path('movie/<int:movie_id>/vote/<int:pk>/', views.UpdateVote.as_view(),
         name='update-vote'),
]
