# from django.shortcuts import render
# from watchlist_app.models import Movie
# from django.views import generic
# from django.http import JsonResponse
# # Create your views here.

# def movie_list(request):
#   movies = Movie.objects.all()
#   data = {'movies': list (movies.values())}
    
#   return JsonResponse(data) 

# def movie_details(request, pk):
#   movie = Movie.objects.get(pk=pk) 
#   data = {
#     'name': movie.name,
#     'description':movie.description,
#     'active': movie.active
#     }
#   return JsonResponse(data)
#   print(movie)
    
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
#   # class movie_list(generic.ListView):
#   #   movies = Movie.objects.all()