# Generated by Django 3.2.5 on 2021-08-02 20:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actual_price', models.FloatField(blank=True, default=None, null=True)),
                ('area', models.FloatField(blank=True, default=None, null=True)),
                ('address', models.TextField(blank=True, default=None, null=True)),
                ('city', models.CharField(blank=True, default=None, max_length=1000, null=True)),
                ('resale', models.BooleanField(blank=True, default=None, null=True)),
                ('bhk', models.IntegerField(blank=True, default=None, null=True)),
                ('rera_approved', models.BooleanField(blank=True, default=None, null=True)),
                ('prop_image', models.ImageField(default=None, upload_to='prop_images')),
                ('no_of_shares', models.IntegerField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proposed_price', models.FloatField(blank=True, default=None, null=True)),
                ('property_details', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='seller_app.property')),
                ('seller_details', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]