# Generated by Django 5.1 on 2024-09-28 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_email_order_first_name_order_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.IntegerField(default=250000, verbose_name='Harga Keseluruhan'),
            preserve_default=False,
        ),
    ]