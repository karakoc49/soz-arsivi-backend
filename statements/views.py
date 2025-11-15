from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from .models import Statement
from .serializers import StatementSerializer

class StatementViewSet(CacheResponseMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Statement.objects.all()
    serializer_class = StatementSerializer
    cache_response_timeout = 60 * 15  # 15 dakika

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['politician', 'statement_type', 'published_at']
    ordering_fields = ['published_at', 'created_at']
    ordering = ['-published_at']
    search_fields = ['content', 'politician__full_name']

    def get_queryset(self):
        queryset = Statement.objects.all()
        politician_id = self.request.query_params.get("politician_id")
        if politician_id:
            queryset = queryset.filter(politician_id=politician_id)
        return queryset
