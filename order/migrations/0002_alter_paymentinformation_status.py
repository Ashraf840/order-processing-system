# Generated by Django 5.0.6 on 2024-05-27 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentinformation',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('S', 'Successful'), ('R', 'Refunded'), ('F', 'Failed')], default='Order Received by Restaurant', max_length=100),
        ),
    ]
