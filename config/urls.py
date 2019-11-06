import notifications.urls
from des import urls as des_url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from rest_framework_swagger.views import get_swagger_view

from sme_coad_apps.contratos.urls import urlpatterns as contrato_url
from sme_coad_apps.core.urls import urlpatterns as core_urls
from sme_coad_apps.users.urls import urlpatterns as usuario_url

schema_view = get_swagger_view(title='API SME COAD')

urlpatterns = [
                  path("docs/", schema_view),
                  path("api-token-auth/", obtain_jwt_token),
                  path("api-token-refresh/", refresh_jwt_token),
                  path("api-token-verify/", verify_jwt_token),
                  path('metrics/', include('django_prometheus.urls')),
                  # Django Admin, use {% url 'admin:index' %}
                  path(settings.ADMIN_URL, admin.site.urls),
                  # User management
                  # path("users/", include("sme_coad_apps.users.urls", namespace="users")),
                  path("accounts/", include("allauth.urls")),
                  path("django-des/", include(des_url)),
                  # Django Notifications
                  path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
                  # Your stuff: custom urls includes go here
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ADDING URLS FROM APPS
urlpatterns += core_urls
urlpatterns += usuario_url
urlpatterns += contrato_url

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
