from django.shortcuts import render

from .models import Files
from .book_info import BookInfo
from rest_framework import viewsets, status
from .serializers import FilesSerializer
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.

class FilesViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer

    @action(detail=True, methods=['post'])
    def increment_downloads(self, request, pk=None):
        file = self.get_object()
        file.downloads += 1
        file.save(update_fields=['downloads'])
        return Response({'downloads': file.downloads}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_book_info(request, book_title):
    book = BookInfo(book_title)
    return Response(book.read_data())


@api_view(['GET'])
def get_book_info_language(request, language, book_title):
    book = BookInfo(book_title, language)
    return Response(book.read_data())
