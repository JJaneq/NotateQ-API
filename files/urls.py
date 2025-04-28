from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('files', FilesViewSet, basename='files')
router.register('categories', CategoryViewSet, basename='categories')
router.register('tags', TagsViewSet, basename='tags')

urlpatterns = [
    path('api/', include(router.urls)),
]
