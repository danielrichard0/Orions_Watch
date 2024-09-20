# Generated by Django 5.1 on 2024-09-24 11:07

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_guest',
            field=models.BooleanField(default=False, verbose_name='Apakah Pesanan Guest'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]