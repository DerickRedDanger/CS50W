from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class listings(models.Model):
    title = models.CharField(unique= True,max_length=75,null=False, blank=False)
    owner = models.ForeignKey(User, default="{{ request.user }}", on_delete=models.CASCADE)
    Sdescription = models.CharField(verbose_name="Short description",max_length=500)
    description = models.TextField(null=False, blank=False)
    image = models.URLField(max_length=200,blank=True)
    initialBid = models.PositiveIntegerField(null=False, blank=False)
    open = models.BooleanField(default= True)
    hBid = models.PositiveIntegerField(default="0",null=False, blank=False)
    followed= models.ManyToManyField(User,blank=True,related_name="watchlist")
    caution = models.TextField(verbose_name="Caution message",max_length=500, blank=True,null=True)
    cImage = models.URLField(verbose_name="Caution image",max_length=200,blank=True,null=True)
    hBidder=models.PositiveSmallIntegerField(blank=True,null=True)

    def __str__(self):
     return f"{self.title}"

class bids(models.Model):
    auction=models.ForeignKey(listings,on_delete=models.CASCADE)
    bid=models.PositiveIntegerField(null=False, blank=False)
    bidders=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
     return f"bid of {self.bid} money for {self.auction} from bidder {self.bidders}"

class comments(models.Model):
    comment=models.TextField(null=False, blank=False)
    auction=models.ForeignKey(listings,on_delete=models.CASCADE)
    user=models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    def __str__(self):
        return f"comment on {self.auction} from {self.user}"

class category(models.Model):
    title = models.CharField( max_length=75)
    auction = models.ManyToManyField(listings,related_name="category", blank=True)
    description = models.TextField(null=False, blank=True)
    def __str__(self):
        return f"{self.title}"
