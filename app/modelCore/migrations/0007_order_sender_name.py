# Generated by Django 4.0.4 on 2023-01-04 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0006_appversion_ios_current_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='sender_name',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]
