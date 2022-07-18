# Generated by Django 3.2.13 on 2022-07-05 05:48

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appUser', '0025_auto_20220704_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='estimate_dd',
            field=models.DateField(default=datetime.date(2022, 7, 12)),
        ),
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='appUser.product'),
        ),
    ]
