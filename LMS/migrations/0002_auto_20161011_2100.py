# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backuprecords',
            name='operator',
            field=models.ForeignKey(blank=True, to='LMS.Admin', null=True),
        ),
    ]
