# Generated by Django 3.1.5 on 2021-06-03 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20210603_1521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='product',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='product',
            field=models.ManyToManyField(blank=True, to='auctions.Product'),
        ),
    ]