# Generated by Django 5.0.6 on 2024-05-27 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='unit_price',
            field=models.FloatField(blank=True, default=2),
            preserve_default=False,
        ),
    ]
