# Generated by Django 4.2 on 2024-02-02 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pay", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userorders",
            name="id",
            field=models.AutoField(
                default=100000000001,
                primary_key=True,
                serialize=False,
                verbose_name="订单id",
            ),
        ),
    ]
