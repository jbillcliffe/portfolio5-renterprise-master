# Generated by Django 5.1.2 on 2024-11-22 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemtype',
            options={'ordering': ['category', 'name'], 'verbose_name': 'Item Type', 'verbose_name_plural': 'Item Types'},
        ),
    ]