from django.urls import path
from .views import DonationListCreateView, ProjectDonationListView

urlpatterns = [
    path('', DonationListCreateView.as_view(), name='donation-list-create'),
    path('projects/<int:project_id>/', ProjectDonationListView.as_view(), name='project-donation-list'),
]