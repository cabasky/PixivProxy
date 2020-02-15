from django.urls import path
from . import views
urlpatterns = [
    path('', views.postid),
    path('<str:artistid>', view=views.artistpage,name='artistpage'),
    path('info/<str:artistid>', view=views.artistinfo),
    path('img/<str:artistid>/<int:mode>', view=views.artistimg, name='headimg'),
    path('bkg/<str:artistid>', view=views.background, name='bkgimg'),
]
