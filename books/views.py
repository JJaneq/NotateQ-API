from rest_framework.decorators import api_view
from rest_framework.response import Response
from .book_info import BookInfo

# Create your views here.
@api_view(['GET'])
def get_book_info(request, book_title):
    book = BookInfo(book_title)
    return Response(book.read_data())


@api_view(['GET'])
def get_book_info_language(request, language, book_title):
    book = BookInfo(book_title, language)
    return Response(book.read_data())