# Generated by Django 5.0.3 on 2024-03-19 11:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=64, verbose_name='文件hash')),
                ('check_hash', models.CharField(max_length=64, verbose_name='验证hash')),
                ('size', models.BigIntegerField(verbose_name='文件大小')),
                ('upload_size', models.BigIntegerField(default=0, verbose_name='已上传大小')),
                ('broken', models.BooleanField(default=True, verbose_name='是否损坏')),
            ],
            options={
                'verbose_name': '文件',
                'verbose_name_plural': '文件',
            },
        ),
        migrations.CreateModel(
            name='FileUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_face', models.BooleanField(null=True, verbose_name='是否有文件封面')),
                ('file_name', models.CharField(max_length=255, verbose_name='文件名')),
                ('file_type', models.CharField(max_length=64, verbose_name='文件类型')),
                ('parent_folder', models.IntegerField(verbose_name='父文件夹')),
                ('is_folder', models.BooleanField(verbose_name='是否为文件夹')),
                ('is_uploaded', models.BooleanField(default=False, verbose_name='是否已上传')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('upload_time', models.DateTimeField(auto_now_add=True, verbose_name='上传时间')),
                ('file', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='file.files', verbose_name='目标文件')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.user', verbose_name='用户id')),
            ],
            options={
                'verbose_name': '用户文件',
                'verbose_name_plural': '用户文件',
            },
        ),
    ]
