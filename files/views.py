from django.shortcuts import render
from .models import Files
from rest_framework import viewsets, status
from .serializers import FilesSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

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