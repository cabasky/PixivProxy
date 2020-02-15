from django.urls import path
from . import views
urlpatterns = [
    path('', views.postid),
    path('<int:workid>/', views.ArtworkId, name='artworkpage'),
    path('img/<str:workid>/<int:mode>', views.img, name='artwork'),
    path('imgs/<str:workid>/<int:mode>/<int:page>', views.imgs, name='artworks'),
    path('picinfo/<str:workid>/', views.Artworkinfo, name='artworkinfo')
]
