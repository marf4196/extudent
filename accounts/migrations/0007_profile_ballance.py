# Generated by Django 3.2.16 on 2023-01-02 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20230102_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='ballance',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]