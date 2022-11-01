import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class NewDocumentTicketManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(enrollment_parameters__isnull=True)

class DocumentsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(enrollment_parameters__isnull=False)

class RDEDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    enrollment_parameters = models.JSONField(null=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    tickets = NewDocumentTicketManager()
    objects = DocumentsManager()

    class Meta:
        verbose_name = "RDE document"
        verbose_name_plural = "RDE documents"
