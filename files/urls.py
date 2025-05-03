from .views import *

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register('files', FilesViewSet, basename='files')
router.register('categories', CategoryViewSet, basename='categories')
router.register('tags', TagsViewSet, basename='tags')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/users/', UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='user-register'),
    path('activate/<uid64>/<token>/', ActivateView.as_view(), name='user-activate'),
    path('download/<str:filename>/', download_file, name='download-file'),
]
