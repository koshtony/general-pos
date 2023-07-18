# Generated by Django 4.1.6 on 2023-07-18 13:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0010_alter_contacts_cont_created_alter_debts_debt_last_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacts',
            name='cont_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 18, 13, 38, 1, 352383)),
        ),
        migrations.AlterField(
            model_name='debts',
            name='debt_last',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 18, 13, 38, 1, 351885)),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='exp_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 18, 13, 38, 1, 349181)),
        ),
        migrations.AlterField(
            model_name='location',
            name='loc_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 18, 13, 38, 1, 350202)),
        ),
        migrations.AlterField(
            model_name='paid',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 18, 13, 38, 1, 348404)),
        ),
        migrations.AlterField(
            model_name='sales',
            name='s_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 18, 13, 38, 1, 347158)),
        ),
        migrations.AlterField(
            model_name='shops',
            name='shop_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 18, 13, 38, 1, 345099)),
        ),
        migrations.AlterField(
            model_name='stocks',
            name='p_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 18, 13, 38, 1, 346321)),
        ),
        migrations.AlterField(
            model_name='stocks',
            name='p_gen',
            field=models.IntegerField(default=2097972686155951413),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='task_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 18, 13, 38, 1, 350677)),
        ),
        migrations.AlterField(
            model_name='transfers',
            name='t_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 18, 13, 38, 1, 349704)),
        ),
    ]
