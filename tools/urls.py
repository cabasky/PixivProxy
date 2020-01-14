from django.urls import path
from . import views
urlpatterns = [
    path('del/', views.delall),
    path('test',views.testtemp),
]
