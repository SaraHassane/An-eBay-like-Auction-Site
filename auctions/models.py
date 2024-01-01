from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    nameOfCategory = models.CharField(max_length= 50)

    def __str__(self):
        return self.nameOfCategory

class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null=True, related_name="userBid")


class Listing(models.Model):
    title = models.CharField(max_length=25)
    description = models.CharField(max_length= 800)
    imageUrl = models.CharField(max_length= 1000)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="priceOfBid")
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank= True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null="True", related_name="watchlist")

    def __str__(self):
        return self.title

class auctionComments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null=True, related_name="userComments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank= True, null=True, related_name="listingComments")
    message = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"


