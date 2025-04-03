from django.shortcuts import render

from .book_info import BookInfo
from .models import Files
from rest_framework import viewsets, status
from .serializers import FilesSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

class FilesViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer


@api_view(['GET'])
def get_book_info(request, book_title):
    book = BookInfo(book_title)
    return Response(book.read_data())

@api_view(['GET'])
def get_book_info_language(request, language, book_title):
    book = BookInfo(book_title, language)
    return Response(book.read_data())
