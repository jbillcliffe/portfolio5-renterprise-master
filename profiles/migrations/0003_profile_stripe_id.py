# Generated by Django 5.1.2 on 2024-11-25 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_profile_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='stripe_id',
            field=models.CharField(blank=True, default='', max_length=254, null=True),
        ),
    ]
