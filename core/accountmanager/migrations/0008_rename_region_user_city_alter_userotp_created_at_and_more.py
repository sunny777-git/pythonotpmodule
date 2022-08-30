# Generated by Django 4.1 on 2022-08-29 10:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountmanager', '0007_user_ip_address_alter_userotp_created_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='region',
            new_name='city',
        ),
        migrations.AlterField(
            model_name='userotp',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 29, 16, 21, 21, 501625)),
        ),
        migrations.AlterField(
            model_name='userotp',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 29, 16, 23, 21, 501625)),
        ),
        migrations.AlterField(
            model_name='usertoken',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 3, 16, 21, 21, 502624)),
        ),
    ]