# Generated by Django 4.0.4 on 2023-03-31 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0020_alter_mtpayinfo_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='mtpayinfo',
            name='query_limit_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]