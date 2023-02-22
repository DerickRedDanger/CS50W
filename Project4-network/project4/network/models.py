from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follow = models.ManyToManyField("self",blank=True,related_name="following",symmetrical=False)
    Pdescription = models.TextField(null=True, blank=True)

    def serialize(self,user):
        try:
            if user.id == self.id:
                print("owner")
                f = "owner"
            elif self in user.follow.all():
                print("following")
                f = "following"
            else:
                print("nfollowing")
                f = "nfollowing"
        except:
            print("not logged")
            f="notlogged"
        print(f"f = {f}")
        return {
            "id": self.id,
            "username": self.username,
            "description": self.Pdescription,
            "f": f,
            "followers": self.following.count(),
        }
        

    def __str__(self):
        return f"{self.username}"

class post(models.Model):
    owner = models.ForeignKey(User, default="{{ request.User.id }}", on_delete=models.CASCADE,related_name="mycomments")
    post = models.TextField(null=False, blank=False)
    image = models.URLField(max_length=300,blank=True)
    like = models.ManyToManyField(User,blank=True,related_name="liked")
    timestamp = models.DateTimeField(auto_now_add=True)
    public = 'pu'
    private = 'pr'
    following = 'fo'
    Privacy_choices = [
        (public, 'Public'),
        (private, 'Private'),
        (following, 'Following'),
    ]
    
    privacy = models.CharField(
        max_length=2,
        choices=Privacy_choices,
        default=public,
    )

    def serialize(self,user):
        if self.image == "":
            Im=False
        else:
            Im="true"
        if user == self.owner:
            own = "true"
        else:
            own = False
        if user in self.like.all():
            like = "true"
        else:
            like = False 
            
        return {
            "id": self.id,
            "post": self.post,
            "owner": self.owner.username,
            "image": self.image,
            "Im":Im,
            "likes": self.like.count(),
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "privacy": self.privacy,
            "own":own,
            "like":like,
            "ownerid":self.owner.id
        }

    def __str__(self):
        return f"Posted by {self.owner} on {self.timestamp}"

class comment(models.Model):
    owner = models.ForeignKey(User, default="{{ request.user}}", on_delete=models.CASCADE,related_name="myposts")
    comment = models.TextField(null=False, blank=False)
    post=models.ForeignKey(post,on_delete=models.CASCADE,related_name="comments")
