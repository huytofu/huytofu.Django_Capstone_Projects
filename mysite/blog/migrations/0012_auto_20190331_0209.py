# Generated by Django 2.1.7 on 2019-03-30 19:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20190331_0147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='create_date',
            field=models.DateField(default=datetime.datetime(2019, 3, 30, 19, 9, 37, 656000, tzinfo=utc)),
        ),
    ]
