# Generated by Django 4.2.3 on 2023-08-01 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("market", "0002_stockownedmodel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stockownedmodel",
            name="number",
            field=models.IntegerField(),
        ),
    ]