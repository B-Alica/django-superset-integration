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
        ...,
    ]

2. Include the superset-integration URLconf in your project urls.py like this::

    path("superset_integration/", include("django_superset_integration.urls")),

3. Generate a Fernet key in a python terminal::

    from cryptography.fernet import Fernet
    FERNET_KEY = Fernet.generate_key()

4. The result is a bytestring like b'jozEHFGLKJHEFUIHEZ4'. **Copy ONLY the content of the string, not the b nor the quotation marks**

5. In your env variables, create a variable **FERNET_KEY** with the copied content as value

6. Run ``python manage.py migrate`` to create the models.

7. Start the development server and visit the admin to create a SupersetInstance and a SupersetDashboard.

8. TODO.