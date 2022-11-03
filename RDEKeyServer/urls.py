from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("RDEDocuments.urls")),
    path("api/", include("RDEDocuments.api.urls")),
    path("saml/", include("djangosaml2.urls")),
    path("admin/", admin.site.urls),
]
