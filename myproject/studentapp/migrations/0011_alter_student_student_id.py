# Generated by Django 4.2.7 on 2024-05-22 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "studentapp",
            "0010_alter_student_first_name_alter_student_last_name_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="student_id",
            field=models.IntegerField(blank=True, max_length=11, null=True),
        ),
    ]
