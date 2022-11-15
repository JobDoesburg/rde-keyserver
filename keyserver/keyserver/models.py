import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class NewDocumentTicketManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(enrollment_parameters__isnull=True)


class DocumentsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(enrollment_parameters__isnull=False)


def validate_enrollment_data(data):
    if not isinstance(data, dict):
        raise ValidationError("Enrollment data must be a dictionary")
    if (
        "n" not in data
        or "Fid" not in data
        or "Fcont" not in data
        or "documentName" not in data
    ):
        raise ValidationError(
            "Enrollment data must contain n, Fid, Fcont and documentName"
        )


class RDEDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    enrollment_parameters = models.JSONField(
        null=True, blank=False, validators=[validate_enrollment_data]
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    objects = DocumentsManager()
    tickets = NewDocumentTicketManager()

    class Meta:
        verbose_name = "RDE document"
        verbose_name_plural = "RDE documents"