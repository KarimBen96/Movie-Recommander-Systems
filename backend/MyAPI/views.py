from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MovieSerializer
from .models import Movie

import pandas as pd
from scipy.sparse import csr_matrix

import csv, json, os, joblib
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))



def make_json(csvFilePath, jsonFilePath):
    data = {}
     
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            key = rows['movieId']
            data[key] = rows
 
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
		'List':'/task-list/',
		'Detail View':'/task-detail/<str:pk>/',
		'Create':'/task-create/',
		'Update':'/task-update/<str:pk>/',
		'Delete':'/task-delete/<str:pk>/',
	    }
    
    # file_path_csv = os.path.join(THIS_FOLDER, 'movies.csv')
    # file_path_json = os.path.join(THIS_FOLDER, 'movies.json')
    # make_json(file_path_csv, file_path_json)
    
    file_path_json = os.path.join(THIS_FOLDER, 'movies.json')
    data = {}
    with open(file_path_json) as json_file:
        data = json.load(json_file)
    
    return Response(data)
    # return Response(api_urls)


@api_view(['GET'])
def movieOverview(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    
    return Response(serializer.data)
    
    
@api_view(['GET'])
def movieOverview(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    
    return Response(serializer.data)


@api_view(['GET'])
def movieDetail(request, pk):
    movies = Movie.objects.get(id=pk)
    serializer = MovieSerializer(movies, many=False)
    
    return Response(serializer.data)


@api_view(['GET'])
def getMovieRecommandations(request):
# def getMovieRecommandations(request, title):
    file_path_model = os.path.join(THIS_FOLDER, 'model_knn.sav')
    loaded_model = joblib.load(file_path_model)
    result = get_movie_recommendation('Iron Man', loaded_model)

    api_urls = {
		'List':'/task-list/',
		'Detail View':'/task-detail/<str:pk>/',
		'Create':'/task-create/',
		'Update':'/task-update/<str:pk>/',
		'Delete':'/task-delete/<str:pk>/',
	    }
    
    print(result)
    return Response(api_urls)
    
    
    
def get_movie_recommendation(movie_name, model):
    n_movies_to_reccomend = 10
    movies = os.path.join(THIS_FOLDER, 'movies.csv')
    movies = pd.read_csv(movies)
    final_dataset = os.path.join(THIS_FOLDER, 'final_dataset.csv')
    final_dataset = pd.read_csv(final_dataset)
    csr_data = csr_matrix(final_dataset.values)
    final_dataset.reset_index(inplace=True)
    
    
    movie_list = movies[movies['title'].str.contains(movie_name)]  
    if len(movie_list):        
        movie_idx = movie_list.iloc[0]['movieId']
        movie_idx = final_dataset[final_dataset['movieId'] == movie_idx].index[0]
        distances, indices = model.kneighbors(csr_data[movie_idx],n_neighbors=n_movies_to_reccomend+1)    
        rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[:0:-1]
        recommend_frame = []
        for val in rec_movie_indices:
            movie_idx = final_dataset.iloc[val[0]]['movieId']
            idx = movies[movies['movieId'] == movie_idx].index
            recommend_frame.append({'Title':movies.iloc[idx]['title'].values[0],'Distance':val[1]})
        df = pd.DataFrame(recommend_frame,index=range(1,n_movies_to_reccomend+1))
        return df
    else:
        return "No movies found. Please check your input"