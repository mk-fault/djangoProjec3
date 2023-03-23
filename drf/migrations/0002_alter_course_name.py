# Generated by Django 4.1.3 on 2023-03-18 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("drf", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="name",
            field=models.CharField(
                help_text="课程名称", max_length=64, unique=True, verbose_name="课程名称"
            ),
        ),
    ]