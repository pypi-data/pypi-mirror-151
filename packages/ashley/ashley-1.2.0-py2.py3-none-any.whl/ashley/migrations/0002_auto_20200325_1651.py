# Generated by Django 3.0.4 on 2020-03-25 16:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lti_toolbox", "0001_initial"),
        ("ashley", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="LTIContext",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("lti_id", models.CharField(db_index=True, max_length=150)),
                (
                    "lti_consumer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="lti_toolbox.LTIConsumer",
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.AddConstraint(
            model_name="lticontext",
            constraint=models.UniqueConstraint(
                fields=("lti_consumer", "id"),
                name="lticontext_unique_consumer_context_id",
            ),
        ),
    ]
