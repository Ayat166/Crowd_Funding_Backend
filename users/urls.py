from django.contrib import admin
from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import *
from .views import activate_account

router = DefaultRouter()
router.register('register', RegisterViewset, basename='register' )
urlpatterns = router.urls

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate_account'),]

