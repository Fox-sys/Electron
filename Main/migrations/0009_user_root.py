# Generated by Django 2.2.5 on 2019-09-30 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0008_auto_20190930_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='root',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
