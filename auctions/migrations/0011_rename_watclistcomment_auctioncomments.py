# Generated by Django 4.2.5 on 2023-09-20 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_rename_listingpage_watclistcomment_listing'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WatclistComment',
            new_name='auctionComments',
        ),
    ]
