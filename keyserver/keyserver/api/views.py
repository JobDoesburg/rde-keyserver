from django.shortcuts import get_object_or_404
from rest_framework import status, serializers, filters
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import RDEDocument


class EnrollmentAPIView(APIView):
    name = "Key server enroll"
    description = "Enroll an RDE document based on a ticket"

    def post(self, request, ticket_id, *args, **kwargs):
        """
        Enroll an RDE document based on a ticket
        :param request: the request
        :param ticket_id: the ticket id
        :param args: args
        :param kwargs: kwargs
        :return: the enrolled RDE document
        """
        ticket = get_object_or_404(RDEDocument.tickets, id=ticket_id)
        ticket.enrollment_parameters = request.data
        ticket.save()
        return Response(status=status.HTTP_201_CREATED, data={"id": ticket.id})


class RDEDocumentSerializer(serializers.ModelSerializer):
    """RDE Document serializer"""

    class Meta:
        model = RDEDocument
        fields = ["enrollment_parameters"]


class DocumentSearchFilter(filters.SearchFilter):
    """RDE Document email search filter for the search API"""

    search_param = "email"
    search_title = "Email"
    search_description = "Email address of the user to search for"

    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)
        if not search_terms:
            return queryset.none()
        return super().filter_queryset(request, queryset, view)


class SearchAPIView(ListAPIView):
    """Search API view"""

    name = "Key server search"
    description = "Search for RDE documents by email"
    serializer_class = RDEDocumentSerializer
    queryset = RDEDocument.objects.all()
    search_fields = ["user__email"]
    filter_backends = (DocumentSearchFilter,)
