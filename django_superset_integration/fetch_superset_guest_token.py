import importlib
import requests
from cryptography.fernet import Fernet

from django.http import HttpResponse
from django.views.decorators.http import require_safe
from django.conf import settings

from .models import SupersetDashboard


def create_rls_clause(user):
    """
    SQL clause to apply to the dashboard data
    Can be adjusted to limit data displayed in the dashboard
    Clause "1=1" apply no filter, so we get all the data
    Clause "1=0" get no data

    Return format : [{"clause": "1=1"}]
    """

    if not user:
        # No data
        return [{"clause": "1=0"}]

    # All data
    return [{"clause": "1=1"}]


@require_safe
def fetch_superset_guest_token(request, dashboard_id: str):
    """
    Get a guest token for integration of a Superset dashboard
    1 - Get an access token
    2 - Get a CSRF token by using the access token
    3 - Get a guest token by using the CSRF token

    Return a HttpResponse with the guest token

    Parameters:
        request
        dashboard_id (str): SupersetDashboard object ID in database
            (not to be confused with attribute integration_id of
            SupersetDashboard object, which is used to integrate the
            dashboard with SupersetEmbeddedSdk)
    """
    # Get a guest_token from Superset API
    # The guest_token allow client access to the Superset dashboard
    with requests.Session() as session:
        dashboard = SupersetDashboard.objects.get(id=int(dashboard_id))
        dashboard_integration_id = dashboard.integration_id
        superset_domain = dashboard.domain.address
        superset_username = dashboard.domain.username

        # Authentication for API access
        url = f"https://{superset_domain}/api/v1/security/login"

        def get_password(password):
            cipher_suite = Fernet(settings.ENCRYPTION_KEY)
            decrypted_password = cipher_suite.decrypt(password.encode())
            return decrypted_password.decode()

        params = {
            "provider": "db",
            "refresh": "True",
            "username": superset_username,
            "password": get_password(dashboard.domain.password),
        }
        session.headers.update({"Content-Type": "application/json"})
        response = session.post(url, json=params)

        access_token = response.json()["access_token"]

        session.headers.update({"Authorization": f"Bearer {access_token}"})
        url = f"https://{superset_domain}/api/v1/security/csrf_token/"
        response = session.get(url)
        csrf_token = response.json()["result"]

        try:
            user = request.user
        except Exception:
            # If no user, no guest_token
            return False

        # SQL clause to apply to the dashboard data
        # Can be adjusted to limit data displayed in the dashboard
        # Clause "1=1" apply no filter, so we get all the data
        # Clause "1=0" get no data
        # the default function can be overridden by creating
        # your own and setting its path in settings.RLS_FUNCTION
        rls_function_path = getattr(settings, "RLS_FUNCTION", None)
        if rls_function_path:
            # Dynamically import the function
            module_path, func_name = rls_function_path.rsplit(".", 1)
            module = importlib.import_module(module_path)
            rls_function = getattr(module, func_name)
        else:
            rls_function = create_rls_clause

        rls = rls_function(user)

        if not rls:
            # If no rls clause, show no data
            rls = [{"clause": "1=0"}]

        # Get guest_token to display the dashboard
        params = {
            "resources": [
                {"id": dashboard_integration_id, "type": "dashboard"}
            ],
            "rls": rls,
            "user": {
                "first_name": "Prenom",
                "last_name": "Nom",
                "username": superset_username,
            },
        }
        headers = {
            "Content-Type": "application/json",
            "X-Csrftoken": csrf_token,
        }
        session.headers.update(headers)
        url = f"https://{superset_domain}/api/v1/security/guest_token/"
        response = session.post(url, json=params)
        guest_token = response.json()["token"]
        return HttpResponse(guest_token)
