# Generated by Django 4.1 on 2022-08-29 10:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountmanager', '0004_user_is_staff_alter_userotp_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_validated',
        ),
        migrations.AlterField(
            model_name='userotp',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 29, 15, 59, 20, 762527)),
        ),
        migrations.AlterField(
            model_name='userotp',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 29, 16, 1, 20, 762527)),
        ),
        migrations.AlterField(
            model_name='usertoken',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 3, 15, 59, 20, 763527)),
        ),
    ]
