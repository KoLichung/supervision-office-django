# Generated by Django 4.0.4 on 2023-01-05 01:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0009_outsideproduct_outsideproductordership'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outsideproduct',
            name='category',
        ),
        migrations.CreateModel(
            name='OutsideCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('suppervisionOffice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelCore.supervisionoffice')),
            ],
        ),
        migrations.AddField(
            model_name='outsideproduct',
            name='outside_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='modelCore.outsidecategory'),
        ),
    ]