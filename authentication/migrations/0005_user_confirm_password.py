# Generated by Django 5.0.7 on 2024-12-08 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_remove_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirm_password',
            field=models.IntegerField(default=0),
        ),
    ]