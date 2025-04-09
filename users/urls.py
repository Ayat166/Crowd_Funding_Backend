from django.contrib import admin
from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import *
from .views import activate_account
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = DefaultRouter()
router.register('register', RegisterViewset, basename='register' )
urlpatterns = router.urls


urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate_account'),
    path('<int:id>/', User_Update_Delete.as_view()),
    path('profile/<int:id>/', ProfileView.as_view(), name='user_profile'),
]
