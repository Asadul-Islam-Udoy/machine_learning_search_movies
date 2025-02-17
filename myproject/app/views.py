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













# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Employee
# from .forms import EmployeeForm

# # CREATE
# def create_employee(request):
#     if request.method == "POST":
#         form = EmployeeForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('employee_list')
#     else:
#         form = EmployeeForm()
#     return render(request, 'employee_form.html', {'form': form})

# # READ (LIST)
# def employee_list(request):
#     employees = Employee.objects.all()
#     return render(request, 'employee_list.html', {'employees': employees})

# # UPDATE
# def update_employee(request, id):
#     employee = get_object_or_404(Employee, id=id)
#     if request.method == "POST":
#         form = EmployeeForm(request.POST, instance=employee)
#         if form.is_valid():
#             form.save()
#             return redirect('employee_list')
#     else:
#         form = EmployeeForm(instance=employee)
#     return render(request, 'employee_form.html', {'form': form})

# # DELETE
# def delete_employee(request, id):
#     employee = get_object_or_404(Employee, id=id)
#     if request.method == "POST":
#         employee.delete()
#         return redirect('employee_list')
#     return render(request, 'confirm_delete.html', {'employee': employee})
