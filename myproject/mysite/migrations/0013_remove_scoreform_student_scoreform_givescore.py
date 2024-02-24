# Generated by Django 4.2.7 on 2024-02-24 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("studentapp", "0005_remove_student_score_studentscore_score"),
        ("mysite", "0012_remove_lecturer_email"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="scoreform",
            name="student",
        ),
        migrations.AddField(
            model_name="scoreform",
            name="givescore",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="studentapp.studentscore",
            ),
        ),
    ]
