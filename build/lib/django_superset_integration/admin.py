from django.contrib import admin
from django.contrib.admin.models import DELETION
from django.utils.html import escape, format_html
from django.urls import reverse

from .models import (
    SupersetInstance,
    SupersetDashboard,
    SupersetIntegrationLogEntry,
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


@admin.register(SupersetIntegrationLogEntry)
class SupersetIntegrationEntryAdmin(admin.ModelAdmin):
    """
    Log entries for creation, modification or deletion made
    to SupersetInstance and SupersetDashboard in admin site
    """

    date_hierarchy = "action_time"

    list_filter = ["action_flag", "content_type"]

    search_fields = ["object_repr", "change_message"]

    list_display = [
        "action_time",
        "user",
        "content_type",
        "object_link",
        "action_flag",
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != "POST"

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse(
                    "admin:%s_%s_change" % (ct.app_label, ct.model),
                    args=[obj.object_id],
                ),
                escape(obj.object_repr),
            )
        return format_html(link)

    object_link.short_description = "Objet concerné"

    def queryset(self, request):
        return super().queryset(request).prefetch_related("content_type")
