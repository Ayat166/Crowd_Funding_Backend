from django.contrib import admin
from django.urls import path
from .views import ProfileView
from .views import DeleteAccountAPIView,  UserUpdateAPIView


urlpatterns = [
    path('delete-account/', DeleteAccountAPIView.as_view(), name='delete_account_api'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='update_user'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='user_profile'),
]
