# Generated by Django 5.0 on 2025-02-02 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("examination", "0002_letter"),
    ]

    operations = [
        migrations.DeleteModel(name="Letter",),
    ]
