# Generated by Django 3.1.5 on 2021-06-02 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210531_2315'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Wishlist',
            new_name='Watchlist',
        ),
    ]
