# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-16 02:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Transmission', '0002_auto_20161009_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textaction',
            name='message_content',
            field=models.TextField(help_text="Message content will be evaluated as a <a href='https://mustache.github.io/mustache.5.html' target='_blank'>mustache template</a>.", max_length=500),
        ),
    ]
