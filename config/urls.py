import notifications.urls

from des import urls as des_url
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path
from django.views import defaults as default_views
from rest_framework import permissions
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from sme_coad_apps.atestes.urls import urlpatterns as ateste_url
from sme_coad_apps.contratos.urls import urlpatterns as contrato_url
from sme_coad_apps.core.urls import urlpatterns as core_urls
from sme_coad_apps.users.urls import urlpatterns as usuario_url

schema_view = get_schema_view(
   openapi.Info(
      title='API SME SAFI',
      default_version='v1',
   ),
   permission_classes=(permissions.IsAdminUser, ),
)

urlpatterns = [
                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  path("api-token-auth/", obtain_jwt_token),
                  path("api-token-refresh/", refresh_jwt_token),
                  path("api-token-verify/", verify_jwt_token),
                  path('metrics/', include('django_prometheus.urls')),
                  # Django Admin, use {% url 'admin:index' %}
                  path(settings.ADMIN_URL, admin.site.urls),
                  # User management
                  path("django-des/", include(des_url)),
                  # Django Notifications
                  path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
                  # Your stuff: custom urls includes go here
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ADDING URLS FROM APPS
urlpatterns += core_urls
urlpatterns += ateste_url
urlpatterns += usuario_url
urlpatterns += contrato_url

# SWAGGER
urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', login_required(schema_view.without_ui(cache_timeout=0)), name='schema-json'),
    re_path(r'^swagger/$', login_required(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    re_path(r'^redoc/$', login_required(schema_view.with_ui('redoc', cache_timeout=0)), name='schema-redoc'),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
