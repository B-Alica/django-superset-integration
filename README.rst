============
django-superset-integration
============

django-superset-integration is a Django app to integration Apache Superset dashboards into a Django application.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "superset-integration" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "django_superset_integration",
    ]

2. Include the superset-integration URLconf in your project urls.py like this::

    path("superset_integration/", include("django_superset_integration.urls")),

3. Run ``python manage.py migrate`` to create the models.

4. Start the development server and visit the admin to create a SupersetInstance and a SupersetDashboard.

5. TODO.