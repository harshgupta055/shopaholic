# Generated by Django 3.2.13 on 2022-06-22 13:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appUser', '0002_alter_customuser_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=300)),
                ('about', models.TextField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('quantity', models.IntegerField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('total_rating', models.BigIntegerField(default=0)),
                ('category', models.ManyToManyField(blank=True, related_name='P_category', to='appUser.Category')),
                ('user_rating', models.ManyToManyField(blank=True, related_name='P_user_rating', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, upload_to='product/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appUser.product')),
            ],
        ),
    ]
