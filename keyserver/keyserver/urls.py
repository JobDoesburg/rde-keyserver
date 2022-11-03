from django.urls import path

from .views import *

urlpatterns = [
    path("", DocumentsView.as_view(), name="documents"),
    path("enroll/", EnrollView.as_view(), name="enroll"),
]
