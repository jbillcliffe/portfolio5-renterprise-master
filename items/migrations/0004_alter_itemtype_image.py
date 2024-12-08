# Generated by Django 5.1.2 on 2024-12-08 00:43

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_itemtype_product_stripe_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtype',
            name='image',
            field=cloudinary.models.CloudinaryField(default='placeholder', max_length=255, verbose_name='image'),
        ),
    ]