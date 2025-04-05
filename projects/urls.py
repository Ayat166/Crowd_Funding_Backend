from django.contrib import admin
from django.urls import path, include
from .views import RatingListCreateView

urlpatterns = [
    path('<int:project_id>/ratings/', RatingListCreateView.as_view(), name='rating-list-create'),
]
