from django_filters import rest_framework as filters
from .models import Files, Category, Books, Tag

class FilesFilter(filters.FilterSet):
    #TODO: make title search instead of filter
    title = filters.CharFilter(lookup_expr='icontains')
    author = filters.CharFilter()
    category = filters.ModelMultipleChoiceFilter(field_name='categories', queryset=Category.objects.all())
    tags = filters.CharFilter(field_name='tags__name')
    upload_date = filters.DateFromToRangeFilter(field_name='upload_date')
    downloads_min = filters.NumberFilter(field_name='downloads', lookup_expr='gte')
    downloads_max = filters.NumberFilter(field_name='downloads', lookup_expr='lte')
    to_delete = filters.BooleanFilter(method='filter_to_delete')
    date = filters.DateFromToRangeFilter(field_name='date')
    rating_min = filters.NumberFilter(field_name='rating', lookup_expr='gte')
    rating_max = filters.NumberFilter(field_name='rating', lookup_expr='lte')
    books = filters.ModelMultipleChoiceFilter(field_name='bibliography__title', queryset=Books.objects.all(), to_field_name='title')
    tags = filters.ModelMultipleChoiceFilter(field_name='tags__name', queryset=Tag.objects.all(), to_field_name='name')

    class Meta:
        model = Files
        fields = ['title', 'author', 'categories', 'tags', 'upload_date', 'downloads', 'delete_time', 'date', 'rating', 'books']

    def filter_to_delete(self, queryset, name, value):
        if value in ['true', True]:
            return queryset.filter(delete_time__isnull=False)
        elif value in ['false', False]:
            return queryset.exclude(delete_time__isnull=False)
        return queryset