from rest_framework import viewsets
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from .models import Topic
from .serializers import TopicSerializer

class TopicViewSet(CacheResponseMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    cache_response_timeout = 3600 * 6  # 6 saat
