# Generated by Django 5.1.2 on 2024-11-22 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Paid'),
        ),
    ]