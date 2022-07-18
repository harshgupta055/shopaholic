# Generated by Django 3.2.13 on 2022-07-07 08:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appUser', '0029_auto_20220705_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='avg_rating',
            field=models.FloatField(blank=True, default=0.0),
        ),
        migrations.AlterField(
            model_name='order',
            name='estimate_dd',
            field=models.DateField(default=datetime.date(2022, 7, 14)),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('Getting Ready for Packing', 'Getting Ready for Packing'), ('Packed', 'Packed'), ('Shipped', 'Shipped'), ('Out for Delivery', 'Out for Delivery'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Requested for Return', 'Requested for Return'), ('Return Approved', 'Return Approved'), ('Returned', 'Returned')], default='Getting Ready for Packing', max_length=30),
        ),
    ]
