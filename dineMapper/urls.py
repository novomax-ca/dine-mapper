from django.contrib import admin
from django.urls import path, include
from map.views import signup, logout_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("map.urls")),
    path("admin/", admin.site.urls),
    path("signup", signup, name="signup"),
    path("logout", logout_view, name="logout"),
    path("__debug__/", include("debug_toolbar.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)