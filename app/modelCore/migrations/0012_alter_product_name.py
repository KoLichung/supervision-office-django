from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0011_remove_orderstate_cashflowstate_order_cashflowstate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
