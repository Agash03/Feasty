# Generated by Django 5.0.7 on 2024-12-13 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_remove_user_confirm_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.IntegerField(default=0),
        ),
    ]