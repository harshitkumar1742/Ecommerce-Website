# Generated by Django 3.2.7 on 2021-11-05 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addtocart',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]