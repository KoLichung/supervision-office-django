# Generated by Django 4.0.4 on 2022-05-30 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0026_remove_order_ordermoney'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='orderMoney',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='productordership',
            name='money',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
