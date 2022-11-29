import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class NewDocumentTicketManager(models.Manager):
    """Manager for new document tickets (documents that have not been enrolled yet)"""

    def get_queryset(self):
        return super().get_queryset().filter(enrollment_parameters__isnull=True)


class DocumentsManager(models.Manager):
    """Manager for enrolled RDE documents"""

    def get_queryset(self):
        return super().get_queryset().filter(enrollment_parameters__isnull=False)


def validate_enrollment_data(data):
    """Validate enrollment data"""
    if not isinstance(data, dict):
        raise ValidationError("Enrollment data must be a dictionary")
    if (
        "documentName" not in data
        or "caOID" not in data
        or "piccPublicKey" not in data
        or "rdeDGId" not in data
        or "rdeRBLength" not in data
        or "rdeDGContent" not in data
        or "securityData" not in data
        or "mrzData" not in data
        or "faceImageData" not in data
    ):
        raise ValidationError(
            "Enrollment data is not valid. Missing one or more required fields"
        )

    # TODO way more validation here (e.g. check that the data types are valid (hexstrings), data size, None values, etc.)
    # Also verify the signature (if present) and the certificate (if present). Full passive authentication should be done here (we dont support active authentication yet)
    # As key server, we might not want to store privacy sensitive data like face images, mrz data in general, or enrollment data without security data, or enrollment data from certain countries



class RDEDocument(models.Model):
    """
    Enrolled RDE document.

    If enrollment_parameters is null, there is no enrolled document (yet),
    but a ticket is available to enroll one via the API.
    """

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
