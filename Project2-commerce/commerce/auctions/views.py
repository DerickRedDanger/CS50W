from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import forms
from django.contrib.auth.decorators import login_required

from .models import User,listings,bids,category,comments


def index(request):
    listing=listings.objects.all()
    return render(request, "auctions/index.html",{"listings":listing})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
# view  that shows listing and allows bidding
def listing(request,id,hBid=0, error="",):
    # gathering all the information that will be used both in post
    # and in get methods

    #shows the comment form, or fill it if throught post
    comment = forms.commentsForm(request.POST or None)

    # check for comments in this listing
    try:
        Comments = comments.objects.filter(auction_id=id)
        # if no comments
    except:
        Comments = 0

    # get the listing throught it's id
    listing = listings.objects.get(id=id)

    # gets all bids
    Bids = bids.objects.all()

    # check if for the highest bid
    try:
        hBid = Bids.filter(auction_id=id).order_by('-bid').values('bid')[:1].get()
        hBid = hBid['bid']
        #if there isn't one
    except:
        hBid=0
        #check for the total amount of bids
    try:
        tBid = Bids.filter(auction_id=id).count()
        # if there isn't any
    except:
        tBid=0
    #find all users that are following this listing and pass it
    #to the template to  check if the user is among them
    lst=listing.followed.all()

    # shows the the minimal bid for this listing
    # check if there is a highest bidder and a failsafe
    # in case someone how the highest is lower than the initial bid
    if hBid > listing.initialBid:
        Bid = hBid
    else:
        Bid = listing.initialBid
    # method is post/ if the use made a bid
    if request.method == "POST":
            #get the bid and check if it's higher than both the initial bid
            # and the highest one 
            Bid = int(request.POST["Bid"])
            if Bid >= hBid and Bid < listing.initialBid:
                error = "Your bid must be equal or higher than the initial bid!"
                return render(request, "auctions/listing.html",{
                    "listing":listing, "hBid":hBid,"error":error,
                    "lst":lst,"Bid":Bid,"tBid":tBid,
                    "comment":comment,"Comments":Comments})
            if Bid <= hBid:
                error = "your bid must be higher than the highest bid"
                return render(request, "auctions/listing.html",{
                    "listing":listing, "hBid":hBid,"error":error,
                    "lst":lst,"Bid":Bid,"tBid":tBid,
                    "comment":comment,"Comments":Comments,})
            # save the new highest bid and who bid it, both on listing  
            listing.hBid = Bid
            listing.hBidder = request.POST["user"]
            listing.save() 
            # and bids
            b=bids(auction_id=listing.id,bidders_id=request.POST["user"],bid=request.POST["Bid"])
            b.save()

            # updates the highest bidder and total amount of bids
            Bids = bids.objects.all()
            try:
                hBid = Bids.filter(auction_id=id).order_by('-bid').values('bid')[:1].get()
                hBid = hBid['bid']
            except:
                hBid=0
            try:
                tBid = Bids.filter(auction_id=id).count()
            except:
                tBid=0
    # render the page both through get and post
    return render(request, "auctions/listing.html",{
        "listing":listing, "hBid":hBid,"error":error,
        "lst":lst,"Bid":Bid,"tBid":tBid,
        "comment":comment,"Comments":Comments,})

#view to create a new listing
@login_required
def new(request):  
    #show the form for creating a new listing
    #or get the form filled throught post
    form = forms.listingsForm(request.POST or None)
    # show all avaliable categories
    categori=category.objects.all()
    # if the form came from post and is valid, save it
    if form.is_valid():
        form.save()
        # than add it to the list of auctions of that category
        cat=category.objects.get(id=request.POST['categorie'])
        auct= listings.objects.get(title=form.cleaned_data['title'])
        cat.auction.add(auct.id)
        # than reset the form to allow the creation of a new listing
        form = forms.listingsForm()
    return render (request, 'auctions/new.html',{
        'form':form,
        'categories':categori,
        },)

#view to close a open form
def close(request,id):
    listing = listings.objects.get(id=id)
    if request.method == "POST":
        listing.open = False
        listing.save()
    return HttpResponseRedirect(reverse("listing",args=(id,)))

# view to save comments created in a listing's page
def comment(request,id):
    if request.method == "POST":
        c=comments(auction_id=id,user_id=request.POST["user"],comment=request.POST["comment"])
        c.save()
    return HttpResponseRedirect(reverse("listing",args=(id,)))

# view to follow/unfollow
def follow(request,id):
    #gets the current listing's id
    auc=listings.objects.get(id=id)

    # check if the follows or not this listing
    # than add/remove him accordingly
    if (request.POST["follow"]) =="Remove":
        auc.followed.remove(request.POST["user"])

    elif(request.POST["follow"]) =="Add":
        auc.followed.add(request.POST["user"])
      
    # save the changes
    auc.save
    return HttpResponseRedirect(reverse("listing",args=(id,)))

# view to show all actegories avaliable
def categories(request):
    listing=category.objects.all()
    return render(request, "auctions/categories.html",{"listings":listing})

# view  to show all listing of a certain category
def Category(request,id):
    categories=category.objects.get(id=id)
    listing=categories.auction.all()
    return render(request, "auctions/Category.html",{"listings":listing,"Category":categories})

# view to show the watchlist of a user
@login_required
def watchlist(request):
    user=request.user
    listing=user.watchlist.all()
    return render(request, "auctions/watchlist.html",{"listings":listing})

    