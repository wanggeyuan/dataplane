# Generated by Django 4.2 on 2024-12-07 06:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("device", "0003_portinfomodel_device_portinfomodel_portname"),
    ]

    operations = [
        migrations.AddField(
            model_name="deviceinfomodel",
            name="deviceName",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
