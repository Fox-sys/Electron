# Generated by Django 2.2.7 on 2020-01-24 14:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0030_auto_20200105_0150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='pub_date_art',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 24, 17, 11, 4, 930993)),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, default=' ', related_name='posts', to='Main.Tag'),
        ),
        migrations.AlterField(
            model_name='commet',
            name='pub_date_com',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 24, 17, 11, 4, 931994)),
        ),
        migrations.AlterField(
            model_name='news',
            name='pub_date_com',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 24, 17, 11, 4, 931994)),
        ),
        migrations.AlterField(
            model_name='tag',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 24, 17, 11, 4, 932994)),
        ),
    ]
