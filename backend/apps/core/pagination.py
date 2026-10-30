from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """20 rows per page; the React app may ask for more with ?page_size=500
    (used to fill dropdown lists)."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def paginate_queryset(self, queryset, request, view=None):
        # A page of an un-ordered query can repeat/skip rows (especially on MySQL).
        if hasattr(queryset, 'ordered') and not queryset.ordered:
            queryset = queryset.order_by('pk')
        return super().paginate_queryset(queryset, request, view)
