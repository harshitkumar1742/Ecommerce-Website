# Generated by Django 3.2.7 on 2021-11-04 03:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('digital', models.BooleanField(blank=True, default=False, null=True)),
                ('categoryname', models.CharField(blank=True, max_length=200, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.product')),
            ],
        ),
    ]
