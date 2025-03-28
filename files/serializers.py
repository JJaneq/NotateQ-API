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
        fields = ['id', 'title', 'description', 'category', 'author', 'upload_date', 'file']

    def validate_file(self, value):
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.pdf', '.docx', '.txt']
        if ext.lower() not in valid_extensions:
            raise ValidationError(f'Nieprawidłowy format pliku. Dozwolone: {", ".join(valid_extensions)}')
        return value
