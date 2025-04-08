from django.urls import path
from .views import get_book_info, get_book_info_language

urlpatterns = [
    path('api/books/search/<slug:book_title>', get_book_info, name='book_info'),
    #FIXME: path with language gives worse results
    #path('api/books/<slug:language>/search/<slug:book_title>', get_book_info_language, name='book_info'),
]