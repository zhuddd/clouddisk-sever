# Generated by Django 4.2 on 2024-02-02 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pay", "0006_userorders_call_back"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userorders",
            name="call_back",
            field=models.CharField(max_length=4096, null=True, verbose_name="回调数据"),
        ),
    ]
