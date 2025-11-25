from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("migrations", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="supersetdashboard",
            name="app_name",
            field=models.CharField(
                "Nom de l'application dans laquelle afficher le dashboard",
                max_length=250,
                blank=True,
                null=True,
            ),
        ),
    ]
