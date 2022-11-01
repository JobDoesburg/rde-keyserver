from django.urls import path

from RDEDocuments.api import views

app_name = "api"

urlpatterns = [
    path("search/", views.SearchAPIView.as_view(), name="search"),
    path("enroll/<uuid:ticket_id>/", views.EnrollmentAPIView.as_view(), name="enroll"),
]
