# Generated by Django 3.2.13 on 2022-07-04 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appUser', '0022_searchhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='deliver_to',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
