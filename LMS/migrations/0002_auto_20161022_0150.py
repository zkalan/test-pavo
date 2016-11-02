# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='availableDays',
            field=models.PositiveIntegerField(default=30),
        ),
        migrations.AlterField(
            model_name='member',
            name='maxBorrowedBooks',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='borrowedTime',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 21, 17, 50, 15, 912000, tzinfo=utc)),
        ),
    ]
