# Generated by Django 4.1.7 on 2023-04-21 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_bid_bid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctionlisting',
            old_name='highestBid',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='auctionlisting',
            name='startingPrice',
        ),
    ]
