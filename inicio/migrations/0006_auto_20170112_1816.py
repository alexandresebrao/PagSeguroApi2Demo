# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-12 18:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0005_auto_20170112_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentpagseguro',
            name='sender_birthday',
            field=models.DateField(blank=True, null=True),
        ),
    ]
