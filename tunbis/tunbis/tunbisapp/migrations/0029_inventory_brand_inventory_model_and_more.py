# Generated by Django 5.1.4 on 2025-03-03 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunbisapp', '0028_reservation_inventory'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='brand',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='inventory',
            name='model',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='inventory',
            name='serial_number',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='brand',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='model',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='serial_number',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
