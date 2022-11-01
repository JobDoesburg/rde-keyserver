from django.urls import path

from RDEDocuments import views

urlpatterns = [
    path("", views.DocumentsView.as_view(), name="documents"),
    path("enroll/", views.EnrollView.as_view(), name="enroll"),
]
