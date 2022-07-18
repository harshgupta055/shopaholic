# Generated by Django 3.2.13 on 2022-06-24 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appUser', '0008_productimage_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomments',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='appUser.product'),
        ),
    ]
