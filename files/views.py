from django.shortcuts import render

from .models import Files, Category
from rest_framework import viewsets, status
from .serializers import FilesSerializer, CategorySerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly

from django.utils import timezone
from datetime import timedelta
from .filters import FilesFilter

# Create your views here.

class FilesViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FilesFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, 
                          IsOwnerOrReadOnly]

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
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'], url_path='files')
    def files(self, request, pk=None):
        category = self.get_object()
        files = Files.objects.filter(category=category)
        serializer = FilesSerializer(files, many=True, context={'request': request})
        return Response(serializer.data)
    
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer