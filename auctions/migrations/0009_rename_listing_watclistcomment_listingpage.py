# Generated by Django 4.2.5 on 2023-09-17 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_bid_bid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watclistcomment',
            old_name='listing',
            new_name='listingPage',
        ),
    ]
