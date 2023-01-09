# Generated by Django 4.1.4 on 2023-01-09 12:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='exp_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 9, 12, 32, 0, 958346, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='exp_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='sales',
            name='s_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 9, 12, 32, 0, 957741, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='sales',
            name='s_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='shops',
            name='shop_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 9, 12, 32, 0, 955655, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='shops',
            name='shop_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='stocks',
            name='p_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 9, 12, 32, 0, 956984, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='stocks',
            name='p_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='transfers',
            name='t_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 9, 12, 32, 0, 958998, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='transfers',
            name='t_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
