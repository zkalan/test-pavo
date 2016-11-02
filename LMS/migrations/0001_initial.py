# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('account', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=6, choices=[(b'male', b'male'), (b'female', b'female')])),
                ('tel', models.CharField(max_length=11)),
                ('photo', models.ImageField(null=True, upload_to=b'photo', blank=True)),
                ('admin_add_date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BackupRecords',
            fields=[
                ('recordId', models.AutoField(serialize=False, primary_key=True)),
                ('fileName', models.CharField(max_length=50)),
                ('operateTime', models.DateTimeField()),
                ('fileSize', models.IntegerField(default=0)),
                ('location', models.CharField(max_length=15)),
                ('operator', models.ForeignKey(blank=True, to='LMS.Admin', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookInfo',
            fields=[
                ('ISBN', models.CharField(max_length=17, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=300)),
                ('author', models.CharField(max_length=200)),
                ('book_image_URL', models.CharField(max_length=200, null=True, blank=True)),
                ('introducton', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookLocation',
            fields=[
                ('locationId', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('floor', models.CharField(max_length=1)),
                ('area', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='BookOnShelf',
            fields=[
                ('bookId', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('state', models.CharField(default=b'in', max_length=10, choices=[(b'in', b'in'), (b'out', b'out')])),
                ('book_add_date', models.DateTimeField()),
                ('bookInfo', models.ForeignKey(to='LMS.BookInfo')),
                ('bookLocation', models.ForeignKey(to='LMS.BookLocation')),
            ],
        ),
        migrations.CreateModel(
            name='Catagory',
            fields=[
                ('catagoryId', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='FrontDeskLibrarian',
            fields=[
                ('account', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=6, choices=[(b'male', b'male'), (b'female', b'female')])),
                ('tel', models.CharField(max_length=11)),
                ('photo', models.ImageField(null=True, upload_to=b'photo', blank=True)),
                ('front_add_date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('account', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=6, choices=[(b'male', b'male'), (b'female', b'female')])),
                ('tel', models.CharField(max_length=11)),
                ('photo', models.ImageField(null=True, upload_to=b'photo', blank=True)),
                ('school', models.CharField(max_length=30)),
                ('type', models.CharField(max_length=20, choices=[(b'undergraduate', b'undergraduate'), (b'postgraduate', b'postgraduate'), (b'faculty', b'faculty')])),
                ('major', models.CharField(max_length=300)),
                ('classNo', models.CharField(max_length=20)),
                ('dueDate', models.DateField()),
                ('maxBorrowedBooks', models.IntegerField(default=10)),
                ('availableDays', models.IntegerField(default=30)),
                ('debt', models.DecimalField(default=0.0, max_digits=4, decimal_places=1)),
                ('bookOwning', models.IntegerField(default=0)),
                ('member_add_date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PublishingHouse',
            fields=[
                ('publisherId', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='StackLibrarian',
            fields=[
                ('account', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=6, choices=[(b'male', b'male'), (b'female', b'female')])),
                ('tel', models.CharField(max_length=11)),
                ('photo', models.ImageField(null=True, upload_to=b'photo', blank=True)),
                ('stack_add_date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransactionRecord',
            fields=[
                ('id', models.CharField(max_length=70, serialize=False, primary_key=True)),
                ('borrowedTime', models.DateTimeField(default=datetime.datetime(2016, 10, 21, 12, 51, 25, 369000, tzinfo=utc))),
                ('returnedTime', models.DateTimeField(null=True, blank=True)),
                ('bookOnShelf', models.ForeignKey(to='LMS.BookOnShelf')),
                ('borrowOperator', models.ForeignKey(related_name='borrowOperator', to='LMS.FrontDeskLibrarian')),
                ('member', models.ForeignKey(to='LMS.Member')),
                ('returnOperator', models.ForeignKey(related_name='returnOperator', blank=True, to='LMS.FrontDeskLibrarian', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='bookinfo',
            name='catagory',
            field=models.ForeignKey(to='LMS.Catagory'),
        ),
        migrations.AddField(
            model_name='bookinfo',
            name='publishingHouse',
            field=models.ForeignKey(to='LMS.PublishingHouse'),
        ),
    ]
