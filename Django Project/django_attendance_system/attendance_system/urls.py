from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from attendance.views import dashboard_router, custom_logout

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/logout/", custom_logout, name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", dashboard_router, name="dashboard_router"),
    path("", include("attendance.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
