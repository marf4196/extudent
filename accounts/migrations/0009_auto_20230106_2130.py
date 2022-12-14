# Generated by Django 3.2.16 on 2023-01-07 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_remove_useridentdocs_ballance'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='rand_int',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]
