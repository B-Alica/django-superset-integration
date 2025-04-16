from django.db import models
from django.conf import settings

from cryptography.fernet import Fernet


# Create your models here.
class SupersetInstance(models.Model):
    """
    Modèle stockant l'adresse de votre instance Superset
    ainsi que l'username permettant d'y accéder
    ...

    Attributes
    ----------
    address: str
        Adresse url de votre instance Superset

    username: str
        Nom d'utilisateur pour accéder à l'instance Superset
        Par défaut : "superset_api"

    password: str
        Mot de passe pour accéder à l'instance Superset

    Methods
    ----------
    set_password(self, raw_password):
        stocke le mot de passe dans le champ mot de passe après l'avoir
        hashé avec django.contrib.auth.hashers.make_password
    """

    address = models.CharField(
        "adresse de l'instance Superset",
        max_length=250,
        blank=False,
        null=False,
        unique=True,
    )

    username = models.CharField(
        "nom d'utilisateur",
        max_length=250,
        blank=False,
        null=False,
        default="superset_api",
    )

    password = models.CharField(
        "mot de passe",
        max_length=128,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Instance Superset : {self.address}"

    def set_password(self, raw_password):
        cipher_suite = Fernet(settings.ENCRYPTION_KEY)
        encrypted_password = cipher_suite.encrypt(raw_password.encode())
        self.password = encrypted_password.decode()


class SupersetDashboard(models.Model):
    """
    Modèle stockant l'ID d'intégration et le nom des dashboards Superset
    qu'on souhaite intégrer dans notre application
    ...

    Attributes
    ----------
    integration_id: str
        ID d'intégration du dashboard Superset
        De la forme xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        où x sont des chiffres et des lettres

    name: str
        Nom du dashboard

    domain: SupersetInstance
        Clé étrangère
        Domaine Superset sur lequel se trouve le dashboard
    """

    integration_id = models.CharField(
        "ID d'intégration",
        max_length=50,
        blank=False,
        null=False,
        unique=True,
    )

    name = models.CharField(
        "Nom",
        max_length=250,
        blank=False,
        null=False,
        unique=True,
    )

    domain = models.ForeignKey(
        SupersetInstance,
        on_delete=models.CASCADE,
        null=False,
    )

    comment = models.TextField(
        "Commentaire",
        blank=True,
        null=True,
    )

    superset_link = models.CharField(
        "Lien vers le dashboard dans Superset",
        max_length=500,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Dashboard : {self.name}"
