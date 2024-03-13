from django.urls import path
from .views import file_view


urlpatterns = [
    path("interact/", file_view, name="file_view"),
]