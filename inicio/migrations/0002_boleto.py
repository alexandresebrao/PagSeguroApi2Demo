# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-11 20:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boleto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
                ('payment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='inicio.PaymentPagSeguro')),
            ],
        ),
    ]
