# Generated by Django 5.0.6 on 2024-05-30 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_address_create_new_shipping_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='create_new_shipping_address',
        ),
    ]