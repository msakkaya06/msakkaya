# Generated by Django 5.1.4 on 2025-03-04 11:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunbisapp', '0029_inventory_brand_inventory_model_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicerequest',
            name='device_type',
            field=models.CharField(choices=[('computer', 'Bilgisayar'), ('display', 'Monitör'), ('printer', 'Yazıcı'), ('color_printer', 'Renkli Yazıcı'), ('scanner', 'Tarayıcı'), ('color_printer_scanner', 'Çok Fonksiyonlu Renkli Yazıcı / Tarayıcı'), ('printer_scanner', 'Çok Fonksiyonlu Siyah Beyaz Yazıcı / Tarayıcı'), ('tablet', 'Tablet Bilgisayar'), ('switch', 'Network Switch Cihazı')], max_length=50),
        ),
        migrations.AlterField(
            model_name='devicerequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Beklemede'), ('approved', 'Onaylandı'), ('rejected', 'Reddedildi'), ('delivered', 'Teslim Edildi')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='device_type',
            field=models.CharField(choices=[('computer', 'Bilgisayar'), ('display', 'Monitör'), ('printer', 'Yazıcı'), ('color_printer', 'Renkli Yazıcı'), ('scanner', 'Tarayıcı'), ('color_printer_scanner', 'Çok Fonksiyonlu Renkli Yazıcı / Tarayıcı'), ('printer_scanner', 'Çok Fonksiyonlu Siyah Beyaz Yazıcı / Tarayıcı'), ('tablet', 'Tablet Bilgisayar'), ('switch', 'Network Switch Cihazı')], max_length=50),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='device_type',
            field=models.CharField(choices=[('computer', 'Bilgisayar'), ('display', 'Monitör'), ('printer', 'Yazıcı'), ('color_printer', 'Renkli Yazıcı'), ('scanner', 'Tarayıcı'), ('color_printer_scanner', 'Çok Fonksiyonlu Renkli Yazıcı / Tarayıcı'), ('printer_scanner', 'Çok Fonksiyonlu Siyah Beyaz Yazıcı / Tarayıcı'), ('tablet', 'Tablet Bilgisayar'), ('switch', 'Network Switch Cihazı')], max_length=50),
        ),
        migrations.CreateModel(
            name='DevicePlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_type', models.CharField(choices=[('computer', 'Bilgisayar'), ('display', 'Monitör'), ('printer', 'Yazıcı'), ('color_printer', 'Renkli Yazıcı'), ('scanner', 'Tarayıcı'), ('color_printer_scanner', 'Çok Fonksiyonlu Renkli Yazıcı / Tarayıcı'), ('printer_scanner', 'Çok Fonksiyonlu Siyah Beyaz Yazıcı / Tarayıcı'), ('tablet', 'Tablet Bilgisayar'), ('switch', 'Network Switch Cihazı')], max_length=50)),
                ('requested_quantity', models.PositiveIntegerField()),
                ('allocated_quantity', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tunbisapp.unit')),
            ],
        ),
    ]
