from django.urls import path
from . import views
urlpatterns = [
    path('', views.searchpage),
    path('illustions/',views.searchWork )
]
