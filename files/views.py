from django.shortcuts import render

from .models import Files
from rest_framework import viewsets, status
from .serializers import FilesSerializer
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.utils import timezone
from datetime import timedelta


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
    
    def destroy(self, request, *args, **kwargs):
        file = self.get_object()
        file.delete_time = timezone.now() + timedelta(days=14)
        file.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
