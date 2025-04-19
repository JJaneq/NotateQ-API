from django.core.exceptions import ValidationError
from django.db import models
import os

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Files(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    #TODO: category -> many to many
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=True, null=True)
    author = models.CharField(max_length=100)
    upload_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='store/files/')
    downloads = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    delete_time = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)

    def clean(self):
        ext = os.path.splitext(self.file.name)[1]
        valid_extensions = ['.pdf', '.docx', '.txt']
        if ext.lower() not in valid_extensions:
            raise ValidationError(f'Nieprawidłowy format pliku. Dozwolone: {valid_extensions}')
