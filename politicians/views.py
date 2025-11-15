from rest_framework import viewsets, filters
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from .models import Politician
from .serializers import PoliticianSerializer

class PoliticianViewSet(CacheResponseMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = PoliticianSerializer
    queryset = Politician.objects.all()
    cache_response_timeout = 3600 * 3  # 3 saat

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    def get_queryset(self):
        queryset = Politician.objects.all()
        party_id = self.request.query_params.get('party_id')
        if party_id:
            queryset = queryset.filter(party_memberships__party_id=party_id)
        return queryset
