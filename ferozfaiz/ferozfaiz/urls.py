from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += i18n_patterns(
    path("", include("core.urls", namespace="core")),
    path("", include("users.urls", namespace="users")),
    path("", include("blogs.urls", namespace="blogs")),
    path("", include("oauth.urls", namespace="oauth")),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
