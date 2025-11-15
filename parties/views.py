from rest_framework import viewsets
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from .models import Party
from .serializers import PartySerializer

class PartyViewSet(CacheResponseMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
    cache_response_timeout = 3600 * 6  # 6 saat
