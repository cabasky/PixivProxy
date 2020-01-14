from django.urls import path
from . import views
urlpatterns = [
    path('info/<str:artistid>',view=views.artistinfo),
    path('img/<str:artistid>/<int:mode>',view=views.artistimg,name='headimg')
]
