# Generated by Django 4.1.6 on 2023-07-18 13:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0008_alter_contacts_cont_created_alter_debts_debt_last_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacts',
            name='cont_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 18, 13, 1, 6, 865073)),
        ),
        migrations.AlterField(
            model_name='debts',
            name='debt_last',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 18, 13, 1, 6, 864591)),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='exp_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 18, 13, 1, 6, 861998)),
        ),
        migrations.AlterField(
            model_name='location',
            name='loc_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 18, 13, 1, 6, 862994)),
        ),
        migrations.AlterField(
            model_name='paid',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 18, 13, 1, 6, 861410)),
        ),
        migrations.AlterField(
            model_name='sales',
            name='s_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 18, 13, 1, 6, 860694)),
        ),
        migrations.AlterField(
            model_name='shops',
            name='shop_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 18, 13, 1, 6, 858716)),
        ),
        migrations.AlterField(
            model_name='stocks',
            name='p_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 18, 13, 1, 6, 859885)),
        ),
        migrations.AlterField(
            model_name='stocks',
            name='p_gen',
            field=models.IntegerField(default=3482069000266043232),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='task_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 18, 13, 1, 6, 863465)),
        ),
        migrations.AlterField(
            model_name='transfers',
            name='t_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 18, 13, 1, 6, 862499)),
        ),
    ]
