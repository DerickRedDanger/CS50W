from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class listings(models.Model):
    title = models.CharField(max_length=75,null=False, blank=False)
    owner = models.ForeignKey(User, related_name="hostedAuction", on_delete=models.CASCADE)
    Sdescription = models.CharField(max_length=500)
    description = models.TextField(null=False, blank=False)
    image = models.URLField(max_length=200,blank=True)
    initialBid = models.PositiveIntegerField(null=False, blank=False)
    open = models.BooleanField(default= True)
    hBid = models.PositiveIntegerField(null=False, blank=False)
    followed= models.ManyToManyField(User,related_name="watchlist")

    def __str__(self):
     return f"{self.title} from {self.owner}"

class bids(models.Model):
    auction=models.ForeignKey(listings,on_delete=models.CASCADE)
    bid=models.PositiveIntegerField(null=False, blank=False)
    bidders=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
     return f"{self.bid} for {self.auction} from {self.bidders}"

class comments(models.Model):
    comment=models.TextField(null=False, blank=False)
    auction=models.ForeignKey(listings,on_delete=models.CASCADE)
    user=models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    def __str__(self):
        return f"comment on {self.auction} from {self.user}"

class category(models.Model):
    title = models.CharField( max_length=75)
    auction = models.ManyToManyField(listings,related_name="category", blank=True)
    def __str__(self):
        return f"{self.title}"