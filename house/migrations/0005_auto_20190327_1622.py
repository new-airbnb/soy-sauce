# Generated by Django 2.1.7 on 2019-03-27 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0004_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='user_id',
        ),
        migrations.AddField(
            model_name='comment',
            name='user_email',
            field=models.CharField(default='', max_length=128),
        ),
    ]
