# Generated by Django 4.1 on 2022-08-29 10:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountmanager', '0006_user_country_user_geo_locations_user_region_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ip_address',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='userotp',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 29, 16, 10, 43, 30615)),
        ),
        migrations.AlterField(
            model_name='userotp',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 29, 16, 12, 43, 30615)),
        ),
        migrations.AlterField(
            model_name='usertoken',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 3, 16, 10, 43, 30615)),
        ),
    ]
