from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("keyserver.urls")),
    path("api/", include("keyserver.api.urls")),
    path("saml/", include("djangosaml2.urls")),
    path("admin/", admin.site.urls),
]
