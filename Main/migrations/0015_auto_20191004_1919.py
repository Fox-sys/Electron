# Generated by Django 2.2.5 on 2019-10-04 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0014_delete_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Nickname_us',
            field=models.CharField(max_length=70, unique=True, verbose_name='Ник'),
        ),
        migrations.AlterField(
            model_name='user',
            name='banned',
            field=models.IntegerField(default=0, verbose_name='Уровень бана'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email_us',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Почта'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password_us',
            field=models.CharField(max_length=100, verbose_name='Пароль'),
        ),
        migrations.AlterField(
            model_name='user',
            name='root_us',
            field=models.BooleanField(default=False, verbose_name='Админ'),
        ),
    ]
