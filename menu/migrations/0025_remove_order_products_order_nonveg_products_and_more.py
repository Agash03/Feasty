# Generated by Django 5.0.7 on 2024-12-13 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0024_remove_order_nonveg_products_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
        migrations.AddField(
            model_name='order',
            name='nonveg_products',
            field=models.ManyToManyField(blank=True, related_name='orders', to='menu.nonvegmenu'),
        ),
        migrations.AlterField(
            model_name='nonvegmenu',
            name='food_type',
            field=models.CharField(choices=[('nv briyani', 'Non Veg Briyani'), ('nv meals', 'Non Veg Meals'), ('nv starters', 'Non Veg Starters'), ('nv fried rice', 'Non Veg Fried Rice'), ('nv dosa', 'Non Veg Dosa'), ('nv rotti', 'Non Veg Rotti'), ('nv gravies', 'Non Veg Gravies'), ('nv snacks', 'Non Veg Snacks')], default='nv briyani', max_length=50),
        ),
    ]
