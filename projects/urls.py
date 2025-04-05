from django.contrib import admin
from django.urls import path, include
from .views import RatingListCreateView
from django.urls import path
from .views import (
    ProjectListCreateView, ProjectDetailView, CancelProjectView, 
    project_list_view, project_detail_view, project_create_view
)

urlpatterns = [
    path('<int:project_id>/ratings/', RatingListCreateView.as_view(), name='rating-list-create'),
    path('', ProjectListCreateView.as_view(), name='project-list-create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('<int:pk>/cancel/', CancelProjectView.as_view(), name='cancel-project'),

    path('projects/', project_list_view, name='project-list'),
    path('projects/<int:pk>/', project_detail_view, name='project-detail'),
    path('projects/create/', project_create_view, name='project-create'),
]
