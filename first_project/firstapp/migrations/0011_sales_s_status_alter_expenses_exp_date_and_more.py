# Generated by Django 4.1.4 on 2023-02-07 12:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0010_alter_expenses_exp_date_alter_location_loc_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='s_status',
            field=models.CharField(default='sold', max_length=100),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='exp_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 7, 12, 45, 16, 340116)),
        ),
        migrations.AlterField(
            model_name='location',
            name='loc_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 7, 12, 45, 16, 341111)),
        ),
        migrations.AlterField(
            model_name='sales',
            name='s_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 7, 12, 45, 16, 339420)),
        ),
        migrations.AlterField(
            model_name='shops',
            name='shop_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 7, 12, 45, 16, 337448)),
        ),
        migrations.AlterField(
            model_name='stocks',
            name='p_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 7, 12, 45, 16, 338603)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='task_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 7, 12, 45, 16, 341584)),
        ),
        migrations.AlterField(
            model_name='transfers',
            name='t_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 7, 12, 45, 16, 340599)),
        ),
    ]