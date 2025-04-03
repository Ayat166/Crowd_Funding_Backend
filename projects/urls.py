from django.contrib import admin
from django.urls import path , include
from .views import *

urlpatterns = [
   
   path('home/' , HomeProjectView.as_view() , name='home'),
   path("categories/", get_categories, name="get_categories"),
   path("category/<int:category_id>/", category_projects, name="category_projects"),
   path('search/', SearchProjectsView.as_view(), name='search_projects'),
    
]
