# django-superset-integration

![PyPI - Version](https://img.shields.io/pypi/v/django-superset-integration)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/B-Alica/django-superset-integration)

![Monthly Downloads](https://img.shields.io/pypi/dm/django-superset-integration)
![Total Downloads](https://img.shields.io/pepy/dt/django-superset-integration)

`django-superset-integration` is a Django app to integration Apache Superset dashboards into a Django application.

## Quick start

1. Add `django_superset_integration` to your `INSTALLED_APPS` setting like this:

```python
INSTALLED_APPS = [
    ...,
    "django_superset_integration",
    ...,
]
```

2. Include the superset-integration URLconf in your project `urls.py` like this:

```python
path("superset_integration/", include("django_superset_integration.urls")),
```

3. You will need a cryptography Fernet key, so you need to install cryptography:

```python
pip install cryptography
```

4. Generate a Fernet key in a python terminal:

```python
from cryptography.fernet import Fernet
FERNET_KEY = Fernet.generate_key()
```

5. The result is a bytestring like `b'jozEHFGLKJHEFUIHEZ4'`. **Copy ONLY the content of the string, not the b nor the quotation marks**

6. In your env variables, create a variable `FERNET_KEY` with the copied content as value

7. Add a variable `ENCRYPTION_KEY` in your `settings.py` referencing your env variable `FERNET_KEY`:

```python
ENCRYPTION_KEY = os.environ.get("FERNET_KEY", "").encode()
```

8. By default, all dashboard data will be displayed. You can override this by creating your own filtering function and adding it in your `settings.py`:

```python
RLS_FUNCTION = "my_app.my_module.create_rls_clause"
```

Your function must take a parameter `user` and return a SQL rls clause like this : `[{"clause": "1=1"}]`
(where you replace 1=1 by the clause you want).

See Superset documentation for more information

9. Make sure that your Superset instance parameter `GUEST_TOKEN_JWT_EXP_SECONDS` is more than 300 (5 minutes). Otherwise it will expire before it can be refreshed. For example, set it to 600 (10 minutes).

10. In the template where you want to integrate the dashboard, add the following at the emplacement where you want the dashboard:

```html
{% load static %}

...

{% include "django_superset_integration/superset-integration.html" %}
```

11. Run `python manage.py migrate` to create the models.

12. Start the development server and visit the admin site to create a `SupersetInstance` object.

    - address: the address of your Superset instance
    - username: the username that allows to connect via api to your instance. By default : superset_api
    You need to have a service account with minimal permissions to embed dashboards. See Superset documentation for more info.
    - password: the password that allows to connect via api to your instance.

13. After you 
have created a `SupersetInstance` object, create a `SupersetDashboard` object.
    - integration_id: the integration id given by Superset to integrate your dashboard
    - name: a name for your dashboard
    - domain: (foreign key) the SupersetInstance object corresponding to the instance where the dashboard is
    - comment: (optional) a plain text comment
    - superset_link: (optional) the link to your dashboard in Superset

14. In the view where you want to integrate the dashboard, in `get_context_data`, add the following:

```python
from django_superset_integration.models import SupersetDashboard

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    ...

    dashboard_name = "THE NAME OF YOUR DASHBOARD FROM STEP 13"
    dashboard = SupersetDashboard.objects.get(name__iexact=dashboard_name)
    context["dashboard_integration_id"] = dashboard.integration_id
    context["dashboard_id"] = dashboard.id
    context["superset_domain"] = dashboard.domain.address

    ...

    return context
```

15. You can personalize the buttons "Fullscreen" and "Quit fullscreen" by giving class names in your view's `get_context_data`:

```python

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    ...

    context["button_fullscreen_classes"] = "myClass1 myClass2"
    context["button_quit_fullscreen_classes"] = "myClass1 myClass2"

    ...

    return context
```

16. That should be it!
