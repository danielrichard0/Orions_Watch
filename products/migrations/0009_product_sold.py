# Generated by Django 5.1 on 2024-09-06 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sold',
            field=models.IntegerField(default=0, verbose_name='Sold'),
        ),
    ]
