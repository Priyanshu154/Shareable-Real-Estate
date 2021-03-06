# Generated by Django 3.2.5 on 2021-08-26 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller_app', '0010_property_nearest_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='property_active',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='property_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='sold_price',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]
