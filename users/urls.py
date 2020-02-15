from django.contrib import admin
from django.urls import path, include
from users import views
urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('discoveryRefresh/',views.discoveryRefresh),
    path('collections/',views.userCollection),
    path('collections/append/',views.collectionAppend),
    path('collections/add/',views.addBookMarkWork),
    path('',views.userMainPage),
]
