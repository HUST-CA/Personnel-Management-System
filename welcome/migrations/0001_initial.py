# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-21 00:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0004_auto_20160921_0001'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='姓名')),
                ('sex', models.IntegerField(choices=[(1, '男'), (0, '女')], verbose_name='性别')),
                ('tel', models.CharField(max_length=11, unique=True, verbose_name='电话')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='邮箱')),
                ('college', models.CharField(max_length=64, verbose_name='专业-年级')),
                ('dormitory', models.CharField(max_length=64, verbose_name='寝室住址')),
                ('introduction', models.TextField(verbose_name='自我介绍')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Department', verbose_name='部门')),
            ],
            options={
                'verbose_name': '报名者',
                'verbose_name_plural': '报名者',
            },
        ),
    ]