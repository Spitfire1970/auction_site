from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction_Listings(models.Model):
    title = models.CharField(max_length=64)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "creator")
    description = models.TextField(default=title)
    starting_bid = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=2, null=True, choices=[("A","Active"), ("I","Inactive")], default="A")
    url_img = models.CharField(max_length=512, blank = True, default="") 
    category = models.CharField(max_length=32,blank=True, default="")
    users_watchlist = models.ManyToManyField(User,blank=True)
    highest_bid = models.DecimalField(max_digits=20, decimal_places=2, blank=True, default=0)

class Bids(models.Model):
    value = models.DecimalField(max_digits=20, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Auction_Listings, on_delete=models.CASCADE)

class Comments(models.Model):
    description = models.TextField()
    listing = models.ForeignKey(Auction_Listings, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    