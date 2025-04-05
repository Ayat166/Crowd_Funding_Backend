from django.contrib import admin
from django.urls import path, include
from .views import CommentListCreateView, CommentReplyCreateView, ReportListCreateView

urlpatterns = [
    path('projects/<int:project_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:comment_id>/replies/', CommentReplyCreateView.as_view(), name='comment-reply-create'),
    path('reports/', ReportListCreateView.as_view(), name='report-list-create'),
]
