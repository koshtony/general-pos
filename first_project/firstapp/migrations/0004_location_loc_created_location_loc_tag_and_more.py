# Generated by Django 4.1.5 on 2023-02-02 10:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0003_alter_expenses_exp_date_alter_sales_s_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='loc_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 2, 13, 56, 15, 391847)),
        ),
        migrations.AddField(
            model_name='location',
            name='loc_tag',
            field=models.CharField(default='not set', max_length=100),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='exp_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 2, 10, 56, 15, 391847, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='sales',
            name='s_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 2, 10, 56, 15, 391847, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='shops',
            name='shop_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 2, 10, 56, 15, 390699, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='stocks',
            name='p_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 2, 10, 56, 15, 391692, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='transfers',
            name='t_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 2, 10, 56, 15, 391847, tzinfo=datetime.timezone.utc)),
        ),
    ]