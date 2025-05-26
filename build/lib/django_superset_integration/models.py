from django.db import models
from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.db.models.signals import pre_save
from django.dispatch import receiver

from cryptography.fernet import Fernet


class SupersetInstance(models.Model):
    """
    SupersetInstance model containing your Superset instance's address
    and the username to access it
    ...

    Attributes
    ----------
    address: str
        Url address of your Superset instance

    username: str
        Username to access your Superset instance
        By default: "superset_api"

    password: str
        Password to access your Superset instance

    Methods
    ----------
    set_password(self, raw_password):
        Set password in password field after hashing it with django.contrib.auth.hashers.make_password
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


@receiver(pre_save, sender=SupersetInstance)
def superset_instance_pre_save_handler(sender, instance, *args, **kwargs):
    """
    SupersetInstance.address should not begin with "http://" or "https://"
    so we remove this part if necessary
    """

    if instance.address.startswith("http://") or instance.address.startswith(
        "https://"
    ):
        instance.address = instance.address.split("//", 1)[1]


class SupersetDashboard(models.Model):
    """
    SupersetDashboard containing the integration ID and
    name of your Superset dashboard
    ...

    Attributes
    ----------
    integration_id: str
        Integratrion ID of your Superset dashboard
        Format : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        where x are numbers and letters

    name: str
        Name of the dashboard

    domain: SupersetInstance
        Foreign key
        Superset instance containing the dashboard

    comment: str
        Free text field for your comments

    superset_link: str
        Link to the dashboard in Superset
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
