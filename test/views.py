from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
import datetime

@api_view(['GET'])
@cache_page(10)  # 10 saniye cachele
def cached_time_view(request):
    now = datetime.datetime.now()
    return Response({'time': now.strftime("%Y-%m-%d %H:%M:%S")})
