# Generated by Django 5.1.4 on 2024-12-26 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuser',
            name='mail_verified',
            field=models.BooleanField(default=False),
        ),
    ]
