from django.contrib import admin

from .models import SupersetInstance, SupersetDashboard
from .forms import SupersetInstanceCreationForm

from .utils import LogChanges


# Register your models here.
@admin.register(SupersetInstance)
class SupersetInstanceAdmin(LogChanges, admin.ModelAdmin):
    """
    Modèle admin pour SupersetInstance
    Nom affiché : "Instance Superset"
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
        Surcharge de admin.ModelAdmin.save_form
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
        Exclure le champ password dans le formulaire de modification
        """
        fields = super().get_fields(request, obj)
        if obj:
            fields.remove("password")
        return fields


@admin.register(SupersetDashboard)
class SupersetDashboardAdmin(LogChanges, admin.ModelAdmin):
    """
    Modèle admin pour SupersetDashboard

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
