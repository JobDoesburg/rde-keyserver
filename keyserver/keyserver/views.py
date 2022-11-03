from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, TemplateView

from .models import RDEDocument


class DocumentsView(LoginRequiredMixin, ListView):
    model = RDEDocument
    template_name = "documents.html"

    def get_queryset(self):
        return RDEDocument.objects.filter(user=self.request.user)


class EnrollView(LoginRequiredMixin, TemplateView):
    template_name = "enroll.html"
    ticket = None

    def get(self, request, *args, **kwargs):
        RDEDocument.tickets.filter(user=request.user).delete()
        self.ticket = RDEDocument.tickets.create(user=self.request.user)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket_url"] = settings.BASE_URL + reverse(
            "api:enroll", args=[self.ticket]
        )
        return context
