# Generated by Django 5.0.1 on 2024-02-18 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_usercookie_default_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercookie',
            name='access_agree',
            field=models.BooleanField(default=True),
        ),
    ]
