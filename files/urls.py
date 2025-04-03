from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('files', FilesViewSet, basename='files')


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/books/search/<slug:book_title>', get_book_info, name='book_info'),
    #FIXME: path with language gives worse results
    #path('api/books/<slug:language>/search/<slug:book_title>', get_book_info_language, name='book_info'),
]
