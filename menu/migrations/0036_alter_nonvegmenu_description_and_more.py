# Generated by Django 5.1.4 on 2024-12-18 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0035_alter_nonvegmenu_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nonvegmenu',
            name='description',
            field=models.TextField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='vegmenu',
            name='description',
            field=models.TextField(max_length=200, null=True),
        ),
    ]