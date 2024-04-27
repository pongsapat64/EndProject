# Generated by Django 4.2.7 on 2024-04-27 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("studentapp", "0008_delete_event"),
        ("mysite", "0018_history"),
    ]

    operations = [
        migrations.AddField(
            model_name="history",
            name="appointment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="mysite.appointment",
            ),
        ),
        migrations.AlterField(
            model_name="history",
            name="student",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="studentapp.student",
            ),
        ),
    ]
