from django.shortcuts import render

from .models import Files, Category, Tag
from rest_framework import viewsets, status
from .serializers import FilesSerializer, CategorySerializer, TagSerializer
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from django.utils import timezone
from datetime import timedelta
from .filters import FilesFilter

from django.http import FileResponse, Http404
import os
from django.conf import settings
from urllib.parse import quote

# Create your views here.

class FilesViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FilesFilter

    @action(detail=True, methods=['post'])
    def increment_downloads(self, request, pk=None):
        file = self.get_object()
        file.downloads += 1
        file.save(update_fields=['downloads'])
        return Response({'downloads': file.downloads}, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        file = self.get_object()
        file.delete_time = timezone.now() + timedelta(minutes=5)
        file.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'], url_path='files')
    def files(self, request, pk=None):
        category = self.get_object()
        files = Files.objects.filter(category=category)
        serializer = FilesSerializer(files, many=True, context={'request': request})
        return Response(serializer.data)
    
class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @action(detail=True, methods=['get'], url_path='tags')
    def show_tags(self, request):
        tags = self.get_object().tags.all()
        serializer = TagSerializer(tags, many=True, context={'request': request})
        return Response(serializer.data)


def download_file(request, filename):

    try:
        file_obj = Files.objects.get(file__contains=filename)
    except Files.DoesNotExist:
        raise Http404("Plik nie istnieje w bazie danych")

    filepath = os.path.join(settings.MEDIA_ROOT, 'store/files', filename)
    if not os.path.exists(filepath):
        raise Http404("Plik fizycznie nie istnieje")


    original_extension = os.path.splitext(filename)[1]
    download_name = f"{file_obj.title}{original_extension}"


    encoded_filename = quote(download_name)

    response = FileResponse(open(filepath, 'rb'), as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{encoded_filename}"'
    return response