from django.urls import path

from .views import *

app_name = "api"

urlpatterns = [
    path("search/", SearchAPIView.as_view(), name="search"),
    path("enroll/<uuid:ticket_id>/", EnrollmentAPIView.as_view(), name="enroll"),
]
