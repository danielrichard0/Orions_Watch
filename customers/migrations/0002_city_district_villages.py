# Generated by Django 5.1 on 2024-09-17 15:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nama Kabupaten/Kota')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.province')),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nama Kecamatan')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.city')),
            ],
        ),
        migrations.CreateModel(
            name='Villages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nama Desa')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.district')),
            ],
        ),
    ]