
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from parties.views import PartyViewSet
from politicians.views import PoliticianViewSet
from statements.views import StatementViewSet
from topics.views import TopicViewSet
from test.views import cached_time_view

router = routers.DefaultRouter()
router.register(r'parties', PartyViewSet)
router.register(r'politicians', PoliticianViewSet)
router.register(r'statements', StatementViewSet)
router.register(r'topics', TopicViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Söylem Arşivi API",
        default_version='v1',
        description="Türkiye Politikacı Söylem Arşivi API Dokümantasyonu",
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    # Swagger UI
    path('swagger(<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += [
    path('api/test-cache/', cached_time_view),
]
