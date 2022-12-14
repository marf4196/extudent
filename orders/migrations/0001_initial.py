# Generated by Django 3.2.16 on 2022-12-31 22:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveBigIntegerField(default=0)),
                ('price', models.PositiveBigIntegerField(default=0)),
                ('description', models.TextField()),
                ('currency', models.CharField(choices=[('USD', 'US DOLLAR'), ('EUR', 'EURO'), ('GBP', 'POUND')], max_length=20)),
                ('status', models.BooleanField(default=False)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_buyer', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
