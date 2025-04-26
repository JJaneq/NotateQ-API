from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('files', FilesViewSet, basename='files')
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('api/', include(router.urls)),
    path('download/<str:filename>/', download_file, name='download-file'),
]
