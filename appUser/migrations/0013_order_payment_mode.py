# Generated by Django 3.2.13 on 2022-06-29 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appUser', '0012_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_mode',
            field=models.CharField(blank=True, choices=[('Wallet', 'Wallet'), ('COD', 'COD')], max_length=10),
        ),
    ]
