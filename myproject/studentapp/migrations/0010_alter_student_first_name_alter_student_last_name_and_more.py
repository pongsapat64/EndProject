# Generated by Django 4.2.7 on 2024-05-22 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("studentapp", "0009_project_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="first_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="last_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="student_project",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="studentapp.project",
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="subject",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]