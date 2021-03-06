# Generated by Django 2.1.7 on 2019-03-18 21:51

from django.db import migrations, models
import django.db.models.deletion
import utils.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_begin', models.DateField(default=utils.utils.get_date_timestamp)),
                ('date_end', models.DateField(default=utils.utils.get_date_timestamp)),
                ('create_at', models.DateTimeField(default=utils.utils.get_time_zone_object)),
            ],
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('place_id', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=64)),
                ('province', models.CharField(choices=[('ON', 'Ontario'), ('QC', 'Quebec'), ('NS', 'Nova Scotia'), ('NB', 'New Brunswick'), ('MB', 'Manitoba'), ('BC', 'British Columbia'), ('PE', 'Prince Edward Island'), ('SK', 'Saskatchewan'), ('AB', 'Alberta'), ('NL', 'Newfoundland and Labrador')], default='ON', max_length=2)),
                ('postcode', models.CharField(max_length=6)),
                ('date_begin', models.DateField(default=utils.utils.get_date_timestamp)),
                ('date_end', models.DateField(default=utils.utils.get_date_timestamp)),
                ('number_of_beds', models.PositiveIntegerField(default=1)),
                ('create_at', models.DateTimeField(default=utils.utils.get_time_zone_object)),
                ('description', models.CharField(default='no description', max_length=200)),
            ],
            options={
                'ordering': ['-create_at'],
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.CharField(max_length=10240000)),
                ('upload_at', models.DateTimeField(default=utils.utils.get_time_zone_object)),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='house.House')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='house.House'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
    ]
