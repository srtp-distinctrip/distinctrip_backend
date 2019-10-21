# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-08-15 16:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0003_questionnaire_route'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='questionnaire',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='operation.Questionnaire', verbose_name='问卷'),
        ),
    ]