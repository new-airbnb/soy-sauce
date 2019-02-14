# Generated by Django 2.1.7 on 2019-02-14 04:08

from django.db import migrations, models
import utils.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(db_index=True, max_length=128)),
                ('password', models.CharField(max_length=64)),
                ('type', models.CharField(choices=[('admin', 'admin'), ('user', 'user')], default='user', max_length=16)),
                ('create_at', models.DateTimeField(default=utils.utils.get_timestamp)),
            ],
        ),
    ]