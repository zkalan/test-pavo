# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0002_auto_20161011_2100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='backuprecords',
            name='id',
        ),
        migrations.AddField(
            model_name='backuprecords',
            name='recordId',
            field=models.IntegerField(default=1, serialize=False, primary_key=True, db_column=b'Fld'),
        ),
    ]
