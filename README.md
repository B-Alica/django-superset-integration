# django-superset-integration

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

7. By default, all dashboard data will be displayed. You can override this by creating your own filtering function and adding it in your `settings.py`:

```python
RLS_FUNCTION = "my_app.my_module.create_rls_clause"
```

Your function must take a parameter `user` and return a SQL rls clause like this : `[{"clause": "1=1"}]`
(where you replace 1=1 by the clause you want).

See Superset documentation for more information

8. Make sure that your Superset instance parameter `GUEST_TOKEN_JWT_EXP_SECONDS` is more than 300 (5 minutes). Otherwise it will expire before it can be refreshed. For example, set it to 600 (10 minutes).

9. In the template where you want to integrate the dashboard, add the following in your `<head>`:

```html
<link href="{% static 'css/ponctual-rejects.css' %}" rel="stylesheet"/>
```

10. Then add the following at the emplacement where you want the dashboard:

```html
{% include "django_superset_integration/superset-integration.html" %}
```

11. In your view's `get_context_data`, add the following:

```python
dashboard_name = my_dashboard
dashboard = SupersetDashboard.objects.get(name__iexact=dashboard_name)
context["dashboard_integration_id"] = dashboard.integration_id
context["dashboard_id"] = dashboard.id
context["superset_domain"] = dashboard.domain.address
```

12. Run `python manage.py migrate` to create the models.

13. Start the development server and visit the admin site to create a `SupersetInstance` object.

14. After you have created a `SupersetInstance` object, create a `SupersetDashboard` object.

15. That should be it!
