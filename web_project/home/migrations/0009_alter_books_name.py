# Generated by Django 3.2.7 on 2021-11-05 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_movies_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
