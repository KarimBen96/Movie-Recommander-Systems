from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('movie-list/', views.movieOverview, name='movie-list'),
    path('movie-detail/<str:id>/', views.movieDetail, name='movie-detail'),
    path('movie-recommandations/<str:id>/', views.getMovieRecommandations, name='movie-recommandations'),
]