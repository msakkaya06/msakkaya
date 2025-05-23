# Generated by Django 5.1.1 on 2024-11-07 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunbisapp', '0015_printerscannerinformation_connection_interface'),
    ]

    operations = [
        migrations.AlterField(
            model_name='printerscannerinformation',
            name='color_mode',
            field=models.CharField(choices=[('Renkli', 'Color'), ('Siyah-Beyaz', 'Monochrome')], default='Siyah-Beyaz', max_length=20),
        ),
        migrations.AlterField(
            model_name='printerscannerinformation',
            name='device_type',
            field=models.CharField(choices=[('Yazıcı', 'Printer'), ('Tarayıcı', 'Scanner'), ('Yazıcı-Tarayıcı', 'Printer-Scanner'), ('Çok Fonksiyonlu Yazıcı Tarayıcı', 'All-In-One Printers')], default='Printer', max_length=75),
        ),
    ]
