from django_filters import rest_framework as filters
from .models import Files, Category

class FilesFilter(filters.FilterSet):
    #title = filters.CharFilter(lookup_expr='iexact')
    author = filters.CharFilter()
    category = filters.ModelMultipleChoiceFilter(field_name='category', queryset=Category.objects.all())
    tags = filters.CharFilter(field_name='tags__name')
    upload_date = filters.DateFromToRangeFilter(field_name='upload_date')
    downloads_min = filters.NumberFilter(field_name='downloads', lookup_expr='gte')
    downloads_max = filters.NumberFilter(field_name='downloads', lookup_expr='lte')
    to_delete = filters.BooleanFilter(method='filter_to_delete')

    class Meta:
        model = Files
        fields = ['title', 'author', 'category', 'tags', 'upload_date', 'downloads', 'delete_time']

    def filter_to_delete(self, queryset, name, value):
        if value in ['true', True]:
            return queryset.filter(delete_time__isnull=False)
        elif value in ['false', False]:
            return queryset.exclude(delete_time__isnull=False)
        return queryset