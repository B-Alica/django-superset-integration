from django.urls import include, path

from .fetch_superset_guest_token import fetch_superset_guest_token

urlpatterns = [
    path(
        "/",
        fetch_superset_guest_token,
        name="guest-token",
    ),
]


# from django.urls import path
# from .views import fetch_superset_guest_token

# urlpatterns = [
#     # Test pour intégration superset
#     path(
#         "guest_token/<int:dashboard_id>/",
#         fetch_superset_guest_token,
#         name="guest-token",
#     ),
# ]
