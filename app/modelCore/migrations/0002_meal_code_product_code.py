# Generated by Django 4.0.4 on 2022-11-29 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
