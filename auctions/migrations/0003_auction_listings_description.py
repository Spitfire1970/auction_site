# Generated by Django 4.2.3 on 2023-07-07 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_listings_comments_bids'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_listings',
            name='description',
            field=models.TextField(default=models.CharField(max_length=64)),
        ),
    ]
