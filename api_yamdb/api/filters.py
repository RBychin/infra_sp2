from django_filters import rest_framework as filters

from reviews.models import Title


class CustomFilter(filters.FilterSet):
    name = filters.Filter(lookup_expr='icontains')
    genre = filters.BaseInFilter(
        field_name='genre__slug',
        lookup_expr='in'
    )
    category = filters.BaseInFilter(
        field_name='category__slug',
        lookup_expr='in'
    )

    class Meta:
        model = Title
        fields = ('name', 'genre', 'category', 'year',)
