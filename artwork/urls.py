from django.urls import path
from . import views
urlpatterns = [
    path('', views.postid),
    path('<int:workid>/', views.ArtworkId, name='artworkpage'),
    path('img/<str:workid>/<int:mode>', views.img, name='artwork'),
    path('picinfo/<str:workid>/', views.Artworkinfo, name='artworkinfo')
]
