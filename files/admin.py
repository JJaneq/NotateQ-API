from django.contrib import admin
from .models import Files, Category, Tag, Books
# Register your models here.
admin.site.register(Files)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Books)