from django.contrib import admin
from django.contrib.admin import register

from RDEDocuments.models import RDEDocument


@register(RDEDocument)
class RDEDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "created",
        "enrollment_parameters",
    )
