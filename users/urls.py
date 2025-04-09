from django.contrib import admin
from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import *
from .views import activate_account
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from django.urls import path
from .views import ProfileView
from .views import DeleteAccountAPIView,  UserUpdateAPIView

router = DefaultRouter()
router.register('register', RegisterViewset, basename='register' )
urlpatterns = router.urls


urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate_account'),
    path('reset-password/', RequestPasswordReset.as_view(), name='request-password'),
    path('reset-password-confirm/<uidb64>/<token>/', ConfirmPasswordReset.as_view(), name='confirm-password'),
    path('delete-account/', DeleteAccountAPIView.as_view(), name='delete_account_api'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='update_user'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='user_profile'),
    path('logout/', LogoutView.as_view(), name='logout_user'),
]
