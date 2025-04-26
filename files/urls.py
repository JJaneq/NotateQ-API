from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('files', FilesViewSet, basename='files')
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/users/', UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('auth/', include('rest_framework.urls')),
]
