# Generated by Django 5.1 on 2024-09-17 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_city_district_villages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(max_length=150, null=True, verbose_name='Nama Kecamatan'),
        ),
    ]
