# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0005_auto_20161012_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backuprecords',
            name='fileName',
            field=models.CharField(max_length=50),
        ),
    ]
