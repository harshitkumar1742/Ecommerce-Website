# Generated by Django 3.2.7 on 2021-11-09 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0041_alter_reviews_rate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='transcation_id',
            new_name='transaction_id',
        ),
    ]
