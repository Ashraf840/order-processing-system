# Generated by Django 5.0.6 on 2024-05-29 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='create_new_shipping_address',
            field=models.BooleanField(default=False),
        ),
    ]