# Generated by Django 4.2.5 on 2023-09-16 17:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing_watchlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='WatclistComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=300)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userComments', to=settings.AUTH_USER_MODEL)),
                ('lisitng', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listingComments', to='auctions.listing')),
            ],
        ),
    ]
