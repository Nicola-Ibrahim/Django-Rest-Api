from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.permissions import AllowAny

handler404 = "core.views.handler404"

API_PREFIX = "api/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(API_PREFIX, include("config.api_urls")),
]


if settings.DEBUG:
    import debug_toolbar
    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view

    schema_view = get_schema_view(
        openapi.Info(
            title="Snippets API",
            default_version="v1",
            description="Test description",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="contact@snippets.local"),
            license=openapi.License(name="BSD License"),
        ),
        url="http://localhost/api/",
        urlconf="config.urls",
        public=True,
        permission_classes=(AllowAny,),
    )

    urlpatterns += [
        path(API_PREFIX, schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
        # path(API_PREFIX + "redoc", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
        path(API_PREFIX + "__debug__/", include(debug_toolbar.urls)),
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
