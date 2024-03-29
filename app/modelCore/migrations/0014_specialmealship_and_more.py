# Generated by Django 4.0.4 on 2023-03-22 02:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0013_specialmeal_specialmealordership'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialMealShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0, null=True)),
                ('money', models.IntegerField(default=0, null=True)),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelCore.meal')),
            ],
        ),
        migrations.RemoveField(
            model_name='specialmeal',
            name='suppervisionOffice',
        ),
        migrations.AddField(
            model_name='specialmeal',
            name='meal',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='modelCore.meal'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='SpecialMealOrderShip',
        ),
        migrations.AddField(
            model_name='specialmealship',
            name='special_meal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.specialmeal'),
        ),
    ]
