# Generated by Django 4.2.5 on 2024-02-29 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0022_alter_stocks_p_gen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocks',
            name='p_gen',
            field=models.BigIntegerField(default=177038979787),
        ),
    ]
