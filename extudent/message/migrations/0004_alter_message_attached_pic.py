# Generated by Django 3.2.16 on 2023-01-06 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0003_auto_20230105_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='attached_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]