from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Files, Category, Tag, Books
import os

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ['id', 'title']

class FilesSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        many=True
    )
    tags = serializers.ListField(
        child=serializers.CharField(), required=False, write_only=True
    )
    tag_names = serializers.SerializerMethodField(read_only=True)

    def get_tag_names(self, obj):
        return [tag.name for tag in obj.tags.all()]

    class Meta:
        model = Files
        fields = ['id', 'title', 'description', 'categories', 'author', 'upload_date', 'file', 'downloads',
                'tags', 'tag_names', 'delete_time', 'bibliography', 'rating', 'rating_count', 'date']
        extra_kwargs = {'downloads': {'read_only': True}, 
                        'delete_time': {'read_only': True},
                        'rating': {'read_only': True},
                        'rating_count': {'read_only': True},
                        }

    def validate_file(self, value):
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.pdf', '.docx', '.txt']
        if ext.lower() not in valid_extensions:
            raise ValidationError(f'Nieprawidłowy format pliku. Dozwolone: {", ".join(valid_extensions)}')

        max_size_mb = 5
        if value.size > max_size_mb * 1024 * 1024:
            raise ValidationError(f'Plik jest za duży! Maksymalny rozmiar to {max_size_mb} MB.')

        return value

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        categories = validated_data.pop('categories', [])
        books_data = validated_data.pop('bibliography', [])
        file_instance = Files.objects.create(**validated_data)

        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name.lower())
            file_instance.tags.add(tag)

           
        if categories:
            file_instance.categories.set(categories)

        for book in books_data:
            book_instance, _ = Books.objects.get_or_create(title=book.title)
            file_instance.bibliography.add(book_instance)

        return file_instance

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        categories = validated_data.pop('categories', [])

        if 'downloads' in validated_data:
            raise serializers.ValidationError("Downloads can't be updated directly.")

        if tags_data is not None:
            current_tags = set(instance.tags.values_list('name', flat=True))
            new_tags = set(tag.lower() for tag in tags_data)


            tags_to_remove = current_tags - new_tags
            instance.tags.remove(*Tag.objects.filter(name__in=tags_to_remove))


            for tag_name in new_tags - current_tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)

        if categories:
            instance.categories.set(categories)

        return super().update(instance, validated_data)