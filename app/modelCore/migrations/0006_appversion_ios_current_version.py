# Generated by Django 4.0.4 on 2023-01-03 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0005_remove_appversion_ios_current_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='appversion',
            name='iOS_current_version',
            field=models.CharField(blank=True, default='', max_length=10, null=True),
        ),
    ]
