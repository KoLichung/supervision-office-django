# Generated by Django 4.0.4 on 2023-03-22 02:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0014_specialmealship_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialmealship',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='modelCore.order'),
            preserve_default=False,
        ),
    ]