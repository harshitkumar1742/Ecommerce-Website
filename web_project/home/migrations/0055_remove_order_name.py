# Generated by Django 3.2.7 on 2021-11-11 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0054_remove_addtocart_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='name',
        ),
    ]
