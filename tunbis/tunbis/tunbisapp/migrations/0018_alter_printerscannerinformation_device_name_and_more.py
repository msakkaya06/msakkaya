# Generated by Django 5.1.4 on 2024-12-26 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunbisapp', '0017_alter_tebsuser_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='printerscannerinformation',
            name='device_name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='printerscannerinformation',
            name='manufacturer',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
