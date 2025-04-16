from django import forms
from django.utils.translation import gettext_lazy as _

from .models import SupersetInstance


class SupersetInstanceCreationForm(forms.ModelForm):
    """
    SupersetInstance creation form
    """

    address = forms.CharField(
        widget=forms.TextInput(
            attrs={"autofocus": True, "required": True, "id": "address-field"}
        )
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"required": True, "id": "username-field"}
        )
    )

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"required": True, id: "password-field"}
        ),
    )

    class Meta:
        model = SupersetInstance
        fields = (
            "address",
            "username",
            "password",
        )
