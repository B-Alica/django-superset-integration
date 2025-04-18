from django.contrib import admin
from django.contrib.admin.models import DELETION
from django.utils.html import escape, format_html
from django.urls import reverse

from .models import (
    SupersetInstance,
    SupersetDashboard,
)
from .forms import SupersetInstanceCreationForm


@admin.register(SupersetInstance)
class SupersetInstanceAdmin(admin.ModelAdmin):
    """
    Admin model for SupersetInstance
    Displayed name: "Instance Superset"

    :model:`SupersetInstance`
    """

    add_form = SupersetInstanceCreationForm
    model = SupersetInstance

    list_display = (
        "address",
        "username",
    )

    list_filter = ("username",)

    search_fields = (
        "address",
        "username",
    )

    ordering = (
        "address",
        "username",
    )

    def save_form(self, request, form, change):
        """
        Override admin.ModelAdmin.save_form
        """
        if not change:
            form.instance = self.model.objects.create(
                address=form.cleaned_data["address"],
                username=form.cleaned_data["username"],
            )
            form.instance.set_password(form.cleaned_data["password"])
        return super().save_form(request, form, change)

    def get_fields(self, request, obj=None):
        """
        Exclude field "password" in change form
        """
        fields = super().get_fields(request, obj)
        if obj:
            fields.remove("password")
        return fields


@admin.register(SupersetDashboard)
class SupersetDashboardAdmin(admin.ModelAdmin):
    """
    Admin model for SupersetDashboard

    :model:`SupersetDashboard`
    """

    list_per_page = 20

    list_display = (
        "name",
        "integration_id",
        "domain",
    )

    ordering = ("name",)

    search_fields = (
        "name",
        "domain",
    )

    list_filter = ("domain",)
