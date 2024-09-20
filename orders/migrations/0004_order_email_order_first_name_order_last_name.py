# Generated by Django 5.1 on 2024-09-24 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_cust_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.CharField(default='danielrichardo103@gmail.com', max_length=250, verbose_name='Alamat Email'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='first_name',
            field=models.CharField(default='Daniel', max_length=150, verbose_name='Nama Depan'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='last_name',
            field=models.CharField(default='Richardo', max_length=150, verbose_name='Nama Belakang'),
            preserve_default=False,
        ),
    ]