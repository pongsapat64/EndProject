# Generated by Django 4.2.7 on 2023-12-21 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mysite", "0007_lecturer_user_projectmanager"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comadviser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="projectadviser",
            name="adviser",
        ),
        migrations.RemoveField(
            model_name="projectadviser",
            name="project",
        ),
        migrations.RemoveField(
            model_name="adviser",
            name="project",
        ),
        migrations.RemoveField(
            model_name="appointment",
            name="project",
        ),
        migrations.RemoveField(
            model_name="projectmanager",
            name="adviser",
        ),
        migrations.RemoveField(
            model_name="projectmanager",
            name="committee",
        ),
        migrations.RemoveField(
            model_name="projectmanager",
            name="project",
        ),
        migrations.RemoveField(
            model_name="scoreform",
            name="committee",
        ),
        migrations.RemoveField(
            model_name="scoreform",
            name="project",
        ),
        migrations.DeleteModel(
            name="AdviserScore",
        ),
        migrations.DeleteModel(
            name="ProjectAdviser",
        ),
        migrations.AddField(
            model_name="comadviser",
            name="adviser",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="mysite.adviser",
            ),
        ),
        migrations.AddField(
            model_name="comadviser",
            name="committee",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="mysite.committee",
            ),
        ),
        migrations.AddField(
            model_name="appointment",
            name="comadviser",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="mysite.comadviser",
            ),
        ),
        migrations.AddField(
            model_name="projectmanager",
            name="comadviser",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="mysite.comadviser",
            ),
        ),
        migrations.AddField(
            model_name="scoreform",
            name="comadviser",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="mysite.comadviser",
            ),
        ),
    ]
