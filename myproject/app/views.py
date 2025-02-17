from django.shortcuts import render
import os
import pickle
import pandas as pd
import requests
from django.http import JsonResponse

# Create your views here.
def getFrom(request):
    file_path = os.path.join(os.path.dirname(__file__), 'movie_dictionary.pkl')  # Absolute path
    with open(file_path, 'rb') as f:
         loaded_data = pickle.load(f)
    movies = pd.DataFrame(loaded_data)
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Extract data from the POST request
        file_path = os.path.join(os.path.dirname(__file__), 'movie_similarity.pkl')  # Absolute path
        with open(file_path, 'rb') as f:
             loaded_similarity = pickle.load(f)
        similarity = pd.DataFrame(loaded_similarity)
        movie = request.POST.get('title')
        index = movies[movies['title']==movie].index[0]
        movies_data = sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])
        movies_lists=[]
        API_KEY = '88be2f175b13065df10fd133a517af82'
        for i in movies_data[1:8]:
            movie_id = i[0]
            response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US')
            if response.status_code == 200:
               data = response.json()
               movies_lists.append({'title':movies.iloc[i[0]].title,'image':f'https://image.tmdb.org/t/p/w500{data['poster_path']}' if data['poster_path'] else None})
        response_data = {
                 'data': movies_lists,
                 'status': 'success'
        }
        return JsonResponse(response_data)
    else:
       movie_titles = movies['title'].tolist()
       return render(request,'home.html',{'data':movie_titles})

