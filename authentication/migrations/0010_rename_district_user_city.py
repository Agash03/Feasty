# Generated by Django 5.0.7 on 2024-12-17 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_user_district_user_landmark_user_state_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='district',
            new_name='city',
        ),
    ]
