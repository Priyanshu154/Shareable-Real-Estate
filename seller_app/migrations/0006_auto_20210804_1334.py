# Generated by Django 3.2.6 on 2021-08-04 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller_app', '0005_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='longitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(blank=True, max_length=70, null=True),
        ),
    ]
