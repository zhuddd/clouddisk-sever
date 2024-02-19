# Generated by Django 4.2 on 2024-02-19 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_captcha"),
    ]

    operations = [
        migrations.AlterField(
            model_name="captcha",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="account.user",
                verbose_name="用户",
            ),
        ),
    ]
