from django.urls import path
from . import views


urlpatterns = [
    path("interact/", views.file_view, name="file_view"),
]