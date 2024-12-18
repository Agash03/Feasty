# Generated by Django 5.0.7 on 2024-12-10 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0009_alter_nonvegmenu_food_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nonvegmenu',
            name='food_type',
            field=models.CharField(choices=[('briyani', 'Briyani'), ('meals', 'Meals'), ('starters', 'Starters'), ('nvfried rice', 'Fried Rice'), ('nvdosa', 'Dosa'), ('nvrotti', 'Rotti'), ('nvgravies', 'Gravies'), ('nvsnacks', 'Snacks')], default='briyani', max_length=50),
        ),
    ]
