# Generated by Django 5.0.6 on 2024-05-30 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_alter_productattribute_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productattribute',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
