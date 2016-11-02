# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0004_auto_20161012_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backuprecords',
            name='recordId',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
