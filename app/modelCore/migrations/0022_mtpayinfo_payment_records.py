# Generated by Django 4.0.4 on 2023-04-02 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0021_mtpayinfo_query_limit_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='mtpayinfo',
            name='payment_records',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
