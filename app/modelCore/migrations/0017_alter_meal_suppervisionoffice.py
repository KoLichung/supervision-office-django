# Generated by Django 4.0.4 on 2023-03-25 01:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0016_remove_specialmeal_info_remove_specialmeal_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='suppervisionOffice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meal', to='modelCore.supervisionoffice'),
        ),
    ]