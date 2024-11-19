# Generated by Django 5.1.2 on 2024-11-10 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_remove_itemtype_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemtype',
            name='sku',
            field=models.CharField(default='MH-', max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='category',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='name',
            field=models.CharField(max_length=60),
        ),
    ]