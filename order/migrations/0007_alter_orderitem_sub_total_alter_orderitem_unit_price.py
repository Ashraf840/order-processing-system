# Generated by Django 5.0.6 on 2024-05-29 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_alter_orderitem_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='sub_total',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='unit_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
