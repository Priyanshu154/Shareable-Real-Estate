# Generated by Django 3.2.6 on 2021-08-12 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller_app', '0009_property_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='nearest_city',
            field=models.ForeignKey(default=894, on_delete=django.db.models.deletion.PROTECT, to='seller_app.city'),
            preserve_default=False,
        ),
    ]
