# Generated by Django 5.1.4 on 2024-12-21 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0004_voices_owner_surname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voices',
            name='language',
        ),
    ]
