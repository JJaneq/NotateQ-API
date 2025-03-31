from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Files, Category
import os

class FilesSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = Files
        fields = ['id', 'title', 'description', 'category', 'author', 'upload_date', 'file', 'downloads']
        extra_kwargs = {'downloads': {'read_only': True}}

    def validate_file(self, value):
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.pdf', '.docx', '.txt']
        if ext.lower() not in valid_extensions:
            raise ValidationError(f'Nieprawidłowy format pliku. Dozwolone: {", ".join(valid_extensions)}')

        max_size_mb = 5
        if value.size > max_size_mb * 1024 * 1024:
            raise ValidationError(f'Plik jest za duży! Maksymalny rozmiar to {max_size_mb} MB.')

        return value

    def update(self, instance, validated_data):
        if 'downloads' in validated_data:
            raise serializers.ValidationError("Downloads can't be updated directly.")
        return super().update(instance, validated_data)