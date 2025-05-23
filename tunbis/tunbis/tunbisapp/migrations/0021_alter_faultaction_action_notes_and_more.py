# Generated by Django 5.1.4 on 2024-12-29 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunbisapp', '0020_faultaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faultaction',
            name='action_notes',
            field=models.TextField(blank=True, null=True, verbose_name='İşlem Notları'),
        ),
        migrations.AlterField(
            model_name='faultaction',
            name='ink_replaced',
            field=models.BooleanField(default=False, null=True, verbose_name='Kartuş Değiştirildi'),
        ),
        migrations.AlterField(
            model_name='faultaction',
            name='os_installed',
            field=models.BooleanField(default=False, null=True, verbose_name='İşletim Sistemi Kuruldu'),
        ),
        migrations.AlterField(
            model_name='faultaction',
            name='other',
            field=models.BooleanField(default=False, null=True, verbose_name='Diğer İşlemler'),
        ),
        migrations.AlterField(
            model_name='faultaction',
            name='paper_jam_fixed',
            field=models.BooleanField(default=False, null=True, verbose_name='Kağıt Sıkışması Giderildi'),
        ),
        migrations.AlterField(
            model_name='faultaction',
            name='part_installed',
            field=models.BooleanField(default=False, null=True, verbose_name='Parça Takıldı'),
        ),
    ]
