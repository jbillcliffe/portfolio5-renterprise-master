# Generated by Django 5.1.2 on 2024-11-10 02:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemtype',
            name='image_url',
        ),
    ]
