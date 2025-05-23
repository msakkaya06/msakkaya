# Generated by Django 5.1.4 on 2025-02-24 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunbisapp', '0026_devicerequest_is_active_alter_devicerequest_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicerequest',
            name='device_type',
            field=models.CharField(choices=[('printer', 'Siyah-Beyaz Yazıcı'), ('color_printer', 'Renkli Yazıcı'), ('printer_scanner', 'Çok Fonksiyonlu Yazıcı / Tarayıcı'), ('color_printer_scanner', 'Çok Fonksiyonlu Renkli Yazıcı / Tarayıcı'), ('scanner', 'Tarayıcı'), ('computer', 'Bilgisayar'), ('tablet', 'Tablet Bilgisayar')], max_length=40),
        ),
    ]
