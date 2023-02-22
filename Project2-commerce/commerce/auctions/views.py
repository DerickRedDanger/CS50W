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

def listing(request,id,hBid=0, error="",):
    comment = forms.commentsForm(request.POST or None)

    try:
        Comments = comments.objects.filter(auction_id=id)
    except:
        Comments = 0
    listing = listings.objects.get(id=id)
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

    lst=listing.followed.all()

    if hBid > listing.initialBid:
        Bid = hBid
    else:
        Bid = listing.initialBid
    if request.method == "POST":

        
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
            listing.hBid = hBid
            listing.hBidder = request.POST["user"]
            listing.save()
            b=bids(auction_id=listing.id,bidders_id=request.POST["user"],bid=request.POST["Bid"])
            b.save()

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
    return render(request, "auctions/listing.html",{
        "listing":listing, "hBid":hBid,"error":error,
        "lst":lst,"Bid":Bid,"tBid":tBid,
        "comment":comment,"Comments":Comments,})

@login_required
def new(request):
    form = forms.listingsForm(request.POST or None)
    categori=category.objects.all()
    if form.is_valid():
        form.save()
        cat=category.objects.get(id=request.POST['categorie'])
        auct= listings.objects.get(title=form.cleaned_data['title'])
        cat.auction.add(auct.id)
        form = forms.listingsForm()
    return render (request, 'auctions/new.html',{
        'form':form,
        'categories':categori,
        },)

def close(request,id):
    listing = listings.objects.get(id=id)
    if request.method == "POST":
        listing.open = False
        listing.save()
    return HttpResponseRedirect(reverse("listing",args=(id,)))


def comment(request,id):
    if request.method == "POST":
        c=comments(auction_id=id,user_id=request.POST["user"],comment=request.POST["comment"])
        c.save()
    return HttpResponseRedirect(reverse("listing",args=(id,)))

def follow(request,id):
    auc=listings.objects.get(id=id)
    if (request.POST["follow"]) =="Remove":

        auc.followed.remove(request.POST["user"])
    elif(request.POST["follow"]) =="Add":

        auc.followed.add(request.POST["user"])
    auc.save
    return HttpResponseRedirect(reverse("listing",args=(id,)))

def categories(request):
    listing=category.objects.all()
    return render(request, "auctions/categories.html",{"listings":listing})

def Category(request,id):
    categories=category.objects.get(id=id)
    listing=categories.auction.all()
    return render(request, "auctions/Category.html",{"listings":listing,"Category":categories})

@login_required
def watchlist(request):
    user=request.user
    listing=user.watchlist.all()
    return render(request, "auctions/watchlist.html",{"listings":listing})

    