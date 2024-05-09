# Generated by Django 5.0.3 on 2024-03-19 11:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('file', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('share_code', models.CharField(max_length=16, verbose_name='分享码')),
                ('share_pwd', models.CharField(blank=True, max_length=16, null=True, verbose_name='分享密码')),
                ('share_time', models.DateTimeField(auto_now_add=True, verbose_name='分享时间')),
                ('share_end_time', models.DateTimeField(blank=True, null=True, verbose_name='分享结束时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('file', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='file.fileuser', verbose_name='分享文件')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.user', verbose_name='分享用户')),
            ],
            options={
                'verbose_name': '分享列表',
                'verbose_name_plural': '分享列表',
            },
        ),
    ]
