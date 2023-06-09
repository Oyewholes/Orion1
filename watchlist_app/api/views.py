from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework .permissions import IsAuthenticated, IsAuthenticatedOrReadOnly 
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle , ScopedRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle,ReviewListThrottle 
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework.exceptions import ValidationError
from rest_framework import generics, mixins 
# from snippets.models import Snippet
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404 
from django_filters.rest_framework import DjangoFilterBackend
from watchlist_app.api.pagination import WatchListPagination, WatchListLOPagination, WatchListCPagination


class UserReview(generics.ListAPIView):
    # queryset = Review.objects.all()   
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated] 
    throttle_classes =[ReviewListThrottle, AnonRateThrottle] 
    # def get_queryset(self):
    #     username = self.kwargs['username'] 
    #     return Review.objects.filter(review_user__username = username)
    
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username = username)  

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated] 
    throttle_classes = [ReviewCreateThrottle]
    
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk') 
        watchlist = WatchList.objects.get(pk=pk)
        review_user = self.request.user 
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user =review_user ) 
        
        if review_queryset.exists():
            raise ValidationError("You have reviewed this particular movie") 
        
        if watchlist.number_rating == 0 :
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2
            
        watchlist.number_rating =  watchlist.number_rating + 1
        watchlist.save()
        
        serializer.save(watchlist=watchlist, review_user= review_user)   

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()   
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated] 
    throttle_classes =[ReviewListThrottle, AnonRateThrottle] 
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username','active']
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist = pk)
            
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes =[ScopedRateThrottle, AnonRateThrottle]
    throttle_scope = "review_detail"  
    
class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]
    
# class StreamPlatformDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = StreamPlatform.objects.all() 
#     serializer_class = StreamPlatformSerializer


# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class StreamPlatformVS(viewsets.ModelViewSet):
    queryset=StreamPlatform.objects.all()
    serializer_class= StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

class StreamPlatformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]
    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform, many = True)
        return Response(serializer.data) 
    
    def post (self, request):
        serizlizer = StreamPlatformSerializer(data=request.data)
        if serizlizer.is_valid():
            serizlizer.save()
            return Response(serizlizer.data)
        else:
            return Response(serizlizer.errors)
        
class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]
    def get(self, request, pk): 
        try:
            movie = StreamPlatform.objects.get(pk=pk) 
        except StreamPlatform.DoesNotExist:
            return Response({'Error':'Movie Not Found'}, status=status.HTTP_404_NOT_FOUND)
          
        serializer = StreamPlatformSerializer(movie)
        return Response(serializer.data)
 
    def put(self, request, pk):
        movie = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(movie, data=request.data) 
        if serializer.is_valid():
           serializer.save() 
           return Response(serializer.data)
        else:
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
    def delete(self, request, pk):  
        movie = StreamPlatform.objects.get(pk=pk) 
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchListCPagination 

class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]
  
    def get(self, request):
      movies = WatchList.objects.all()
      serializer = WatchListSerializer(movies, many =True)
      return Response(serializer.data)

    def post(self, request):
      serializer = WatchListSerializer(data=request.data) 
      if serializer.is_valid():
         serializer.save() 
         return Response(serializer.data)
      else:
           return Response(serializer.errors)    

class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]
    
    def get(self, request, pk): 
     try:
        movie = WatchList.objects.get(pk=pk) 
     except WatchList.DoesNotExist:
          return Response({'Error':'Movie Not Found'}, status=status.HTTP_404_NOT_FOUND) 
          
     serializer = WatchListSerializer(movie)
     return Response(serializer.data)
 
    def put(self, request, pk):
      movie = WatchList.objects.get(pk=pk)
      serializer = WatchListSerializer(movie, data=request.data) 
      if serializer.is_valid():
          serializer.save() 
          return Response(serializer.data)
      else:
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
    def delete(self, request, pk):  
      movie = WatchList.objects.get(pk=pk) 
      movie.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
      
      



# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
      
#       movies = Movie.objects.all()
#       serializer = MovieSerializer(movies, many = True)  
#       return Response(serializer.data) 

#     if request.method == 'POST':
#       serializer = MovieSerializer(data=request.data) 
#       if serializer.is_valid():
#         serializer.save() 
#         return Response(serializer.data)
#       else:
#         return Response(serializer.errors)     
      
      

# @api_view(['GET', 'PUT', 'DELETE']) 
# def movie_details(request, pk):
  
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk) 
#         except Movie.DoesNotExist:
#             return Response({'Error':'Movie Not Found'}, status=status.HTTP_404_NOT_FOUND)
          
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
      
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data) 
#         if serializer.is_valid():
#           serializer.save() 
#           return Response(serializer.data)
#         else:
#           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    
#     if request.method == 'DELETE':
#        movie = Movie.objects.get(pk=pk) 
#        movie.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT) 