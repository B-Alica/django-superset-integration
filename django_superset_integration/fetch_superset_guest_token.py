from django.http import HttpResponse
from django.views.decorators.http import require_safe
from django.conf import settings

import requests
from cryptography.fernet import Fernet

from .models import SupersetDashboard


@require_safe
def fetch_superset_guest_token(request, dashboard_id: int):
    """
    Fonction qui récupère un guest token pour l'intégration
    d'un dashboard Superset
    1 - Récupère un access token
    2 - Récupère un CSRF token en utilisant l'access token
    3 - Récupère un guest token en utilisant le CSRF token

    Retourne une HttpResponse avec le guest token

    Parameters:
        request
        dashboard_id (int): L'ID de l'objet SupersetDashboard dans
        la base de données
            (ne pas confondre avec l'attribut integration_id de
            l'objet SupersetDashboard, qui sert à
            intégrer le dashboard avec SupersetEmbeddedSdk)
    """
    # Récupère un guest_token via l'API Superset
    # Ce guest_token permet l'accès du client au dashboard Superset
    with requests.Session() as session:
        dashboard = SupersetDashboard.objects.get(id=dashboard_id)
        dashboard_integration_id = dashboard.integration_id
        superset_domain = dashboard.domain.address
        superset_username = dashboard.domain.username

        # Authentification pour accès a l'API
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

        cookie = response.headers["set-cookie"].split("; ")[0]
        # Recuperation du guest_token pour l'affichage du diagramme
        params = {
            "resources": [
                {"id": dashboard_integration_id, "type": "dashboard"}
            ],
            "rls": [
                {
                    # Clause SQL appliquée à la récupération des donnes du
                    # dashboard
                    # Elle peut être ajustée pour limiter les données
                    # affichées dans le dashboard en fonction du profil
                    # utilisateur
                    # La valeur "1=1" permet de n'appliquer aucun filtre
                    "clause": "1=1"
                }
            ],
            "user": {
                "first_name": "Prenom",
                "last_name": "Nom",
                "username": superset_username,
            },
        }
        headers = {
            "Content-Type": "application/json",
            "X-Csrftoken": csrf_token,
            "Cookie": cookie,
        }
        session.headers.update(headers)
        url = f"https://{superset_domain}/api/v1/security/guest_token/"
        response = session.post(url, json=params)
        guest_token = response.json()["token"]
        return HttpResponse(guest_token)
