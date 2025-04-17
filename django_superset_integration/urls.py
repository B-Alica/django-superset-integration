from django.urls import path

from .fetch_superset_guest_token import fetch_superset_guest_token

urlpatterns = [
    path(
        "guest_token/<slug:dashboard_id>",
        fetch_superset_guest_token,
        name="guest-token",
    ),
]
