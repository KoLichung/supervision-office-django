# Generated by Django 4.0.4 on 2022-05-20 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0020_remove_order_isatm_order_cvsinfopayfrom_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='supervisionOffice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='modelCore.supervisionoffice'),
        ),
    ]
