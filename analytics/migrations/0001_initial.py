# Generated by Django 4.2.5 on 2023-10-05 08:41

import django.db.models.deletion
import timescale.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PointerPositionEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', timescale.db.models.fields.TimescaleDateTimeField(interval='1 day')),
                ('x', models.IntegerField(default=0, verbose_name='X')),
                ('y', models.IntegerField(default=0, verbose_name='Y')),
                ('browser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.browser')),
            ],
            options={
                'verbose_name': 'Position Event',
                'verbose_name_plural': 'Position Events',
                'db_table': 'pointer_position_event',
            },
        ),
    ]