from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from MyAPI.serializers import MovieSerializer
from MyAPI.models import Movie

import pandas as pd
from scipy.sparse import csr_matrix

import csv, json, os, joblib
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


def id_to_movie_title(id):
    movie = Movie.objects.get(id=pk)
    serializer = MovieSerializer(movie, many=False)

    return movie

print(id_to_movie_title(2))



