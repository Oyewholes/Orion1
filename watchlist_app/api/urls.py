from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter 
# from watchlist_app.api.views import movie_list, movie_details , 
from watchlist_app.api.views import WatchListAV, WatchDetailAV, StreamPlatformAV, StreamPlatformDetailAV, ReviewList, ReviewDetail, ReviewCreate, UserReview, WatchListGV, StreamPlatformVS

router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform')

app_name = 'watchlist_app'

urlpatterns = [
    path("movies/", WatchListAV.as_view(), name='movie-list'),
    path('movies/<int:pk>/', WatchDetailAV.as_view(), name = 'movie-detail'),
    path("movies2/", WatchListGV.as_view(), name='watch-list'),
    
    path('', include(router.urls)),
    
    # re_path("^stream/$", StreamPlatformAV.as_view(), name = 'stream'), 
    # path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(), name = 'stream-detail'),
    
    path("<int:pk>/reviews/", ReviewList.as_view(), name='review-list'),
    path("<int:pk>/review-create/", ReviewCreate.as_view(), name='review-create'),
    path("review/<int:pk>/", ReviewDetail.as_view(), name='review-detail'),
    path("reviews/", UserReview.as_view(), name='user-review-detail')
]

# 
#  re_path("^review/$", ReviewList.as_view(), name = 'review-list'),
#    path("review/<int:pk>", ReviewDetail.as_view(), name = 'review-detail'),  