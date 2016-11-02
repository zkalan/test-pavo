# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0003_auto_20161012_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backuprecords',
            name='recordId',
            field=models.AutoField(default=1, serialize=False, primary_key=True),
        ),
    ]
