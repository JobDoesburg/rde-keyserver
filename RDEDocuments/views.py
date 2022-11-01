from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView

from RDEDocuments.models import RDEDocument


class DocumentsView(LoginRequiredMixin, ListView):
    model = RDEDocument
    template_name = "documents.html"

    def get_queryset(self):
        return RDEDocument.objects.filter(user=self.request.user)


class EnrollView(LoginRequiredMixin, TemplateView):
    template_name = "enroll.html"
    ticket = None

    def dispatch(self, request, *args, **kwargs):
        RDEDocument.tickets.filter(user=request.user).delete()
        self.ticket = RDEDocument.tickets.create(user=self.request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket"] = self.ticket
        return context
