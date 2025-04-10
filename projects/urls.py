from django.contrib import admin
from django.urls import path, include
from django.urls import path
from .views import *

urlpatterns = [
    path('<int:project_id>/ratings/', RatingListCreateView.as_view(), name='rating-list-create'),
    path('', ProjectListCreateView.as_view(), name='project-list-create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('<int:pk>/cancel/', CancelProjectView.as_view(), name='cancel-project'),

   path('home/' , HomeProjectView.as_view() , name='home'),
   path("categories/", get_categories, name="get_categories"),
   path("category/<int:category_id>/", category_projects, name="category_projects"),
   path('search/', SearchProjectsView.as_view(), name='search_projects'),

   path('admin/feature-project/', AdminFeatureProjectView.as_view(), name='admin-feature-project'),
   path('<int:pk>/', ProjectFeatureUpdateView.as_view(), name='update-project-feature'),

]
