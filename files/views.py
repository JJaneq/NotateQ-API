import os
from datetime import timedelta

from .models import Files, Category, Tag, Comment
from .filters import FilesFilter
from .permissions import IsOwnerOrReadOnly
from .serializers import FilesSerializer, CategorySerializer, UserSerializer, TagSerializer, CommentSerializer

from django.http import FileResponse, Http404
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from rest_framework import viewsets, status, generics, permissions 
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from urllib.parse import quote


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
        

    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        file = self.get_object()
        try:
            new_rating = float(request.data.get('rating'))
            if not (0 <= new_rating <= 5):
                return Response({'error': 'Ocena musi być w zakresie 0-5'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError):
            return Response({'error': 'Nieprawidłowa wartość oceny'}, status=status.HTTP_400_BAD_REQUEST)


        total = file.rating * file.rating_count
        file.rating_count += 1
        file.rating = (total + new_rating) / file.rating_count
        file.save(update_fields=['rating', 'rating_count'])

        return Response({
            'rating': file.rating,
            'rating_count': file.rating_count
        }, status=status.HTTP_200_OK)


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
      
# Users  views
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        return Response({
            'username': user.username,
            'email': user.email,
        }, status=status.HTTP_201_CREATED)

class ActivateView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, uid64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is None:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response('Account activated', status=status.HTTP_200_OK)
        else:
            return Response('Activation link is invalid', status=status.HTTP_400_BAD_REQUEST) 

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    

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
