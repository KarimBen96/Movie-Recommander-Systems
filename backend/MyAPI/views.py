from django.shortcuts import render
from . forms import MyForm
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from .models import Movie
from .serializers import MovieSerializers
import pickle
from sklearn.externals import joblib
import json
import numpy as np
from sklearn import preprocessing
import pandas as pd


class MovieView(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializers
    
def myForm(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            myForm = form.save(commit=False)
    else:
        form = MyForm()
    
@api_view(['POST'])

