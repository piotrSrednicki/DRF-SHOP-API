from django_filters import FilterSet, NumberFilter, CharFilter, ModelChoiceFilter
from clientSeller.models import ProductCategory, Product


class ProductFilterSet(FilterSet):
    price = NumberFilter(field_name='price')
    name = CharFilter(field_name='name')
    description = CharFilter(field_name='description')
    category = ModelChoiceFilter(queryset=ProductCategory.objects.all(), field_name='category')

    class Meta:
        model = Product
        fields = ['price', 'name', 'description', 'category']