# Generated by Django 5.1 on 2024-10-10 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_product_sold'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sold',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Barang Terjual'),
        ),
    ]
