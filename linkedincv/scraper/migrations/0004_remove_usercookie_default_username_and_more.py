# Generated by Django 5.0.1 on 2024-02-21 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0003_usercookie_access_agree'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercookie',
            name='default_username',
        ),
        migrations.RemoveField(
            model_name='userprofilehtml',
            name='target',
        ),
    ]
