# Generated by Django 3.2.16 on 2022-12-31 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20221230_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
    ]