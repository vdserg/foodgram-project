from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

from .views import e_handler404, e_handler500

handler404 = e_handler404
handler500 = e_handler500

urlpatterns = [
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("", include("recipes.urls")),
    path("about/", include("django.contrib.flatpages.urls")),
    path(
        "about-author/",
        views.flatpage,
        {"url": "/about-author/"},
        name="about_author",
    ),
    path(
        "about-spec/",
        views.flatpage,
        {"url": "/about-spec/"},
        name="about_spec",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
