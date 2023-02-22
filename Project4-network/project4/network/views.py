from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from . import forms
from .models import User, post,comment
from django.db.models import Max
import json
from django.views.decorators.csrf import csrf_exempt

# index page, loads the initial page and the post creating form 
def index(request):
    npost = forms.postForm(request.POST or None)
    return render(request, "network/index.html",{"npost":npost})

# view responsible for saving the new posts
def posts(request):
    if request.method == "POST":
        npost = forms.postForm(request.POST)
        # if post is valid, save it and reset the one in page.
        if npost.is_valid():
            pst = request.POST['post']
            image = request.POST['image']
            privacy = request.POST['privacy']
            owner = getattr(request, "user", None)
            post.objects.create(post=pst, image=image,privacy=privacy,owner=owner)
            print(f"post = {pst}, image = {image},privacy = {privacy},owner = {owner}")
            npost = forms.postForm(None)
        else:
        # if it's not, render the same page with the error
            return render(request, "network/index.html",{"npost":npost})
            
        return HttpResponseRedirect(reverse("index"))

    else:
        return HttpResponseRedirect(reverse("index"))

# view to edit posts
# since i was unable to add the csrf inside each post, I made it 
# not need it and instead check if the user that edited is the owner
@csrf_exempt
def edit(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        P = post.objects.get(id=data.get("np"))
        # if the user that submitted is the post's owner
        if P.owner == request.user:
            P.post = data.get("post")
            P.image = data.get("image")
            P.privacy = data.get("privacy")
            P.save()
        # else return an error 
        else:
            return JsonResponse({"error": "User is not the owner of this post."})

        return JsonResponse({"OK": "All good"})

    else:
        return JsonResponse({"error": "PUT only"})

# view to edit the pesonal page's description
# works akin to edit. 
@csrf_exempt
def description(request,id):
    if request.method == "PUT":
        data = json.loads(request.body)
        d = User.objects.get(id=id)
        if d == request.user:
            d.Pdescription = data.get("description")
            d.save()
        else:
            return JsonResponse({"error": "User is not the owner of this page."})

        return JsonResponse({"OK": "All good"})

    else:
        return JsonResponse({"error": "PUT only"})

# view to load posts, pagination was made manually instead of
# using Django 
def getpposts(request):
    # Get the page, privacy and user(if loadin a personal page)
    page = int(request.GET.get("page") or 1)
    privacy = request.GET.get("privacy") or "public"
    user = int(request.GET.get("user") or -1)

    # based on the page, get the first and last posts
    last = (page * 10) 
    first = last - 10
     
    # data is all the information that will be sent in the jsonresponse
    data={}
    # Since i had a hard time interacting inside that data using the name/number
    # of each posts, I create a variable N to hold their name/number 
    n= []

    # if loking at the all posts page
    if privacy == "public":
        # check if the user is logged
        try:
            # if he is:
            # filter for posts of the user
            own = post.objects.filter(owner = request.user.id)
            # filter for follow only post from ppl the user follows
            f = post.objects.filter(privacy = "fo").filter(owner__in = request.user.follow.all())
            # filtering for public posts
            t = post.objects.filter(privacy = "pu")
            # join all queries without dupplicates, ordering by the latest id,
            t = t.union(f,own).order_by("-id")
            print(f"length of t,p,on = {len(t)}")
        except:
            # if he is not logged:
            # then use only the public posts, ordering by the highest Id
            t = post.objects.filter(privacy = "pu").order_by("-id")
            print(f"length of t,p,off = {len(t)}")

    # if set to follow only
    elif privacy == "following":
        # show only post from ppl the user follows
        # both the ones set to public
        p = post.objects.filter(privacy = "pu").filter(owner__in = request.user.follow.all())
        # and the ones set to follower only
        f = post.objects.filter(privacy = "fo").filter(owner__in = request.user.follow.all())
        # than join them
        t = p.union(f).order_by("-id")
        print(f"length of t,f = {len(t)}")

    # if set to personal only
    elif privacy =="personal":
        # get the page owner's id
        o = User.objects.get(id=user)
        # check if the user is logged
        try:
            # if he is, check if he is the owner of the page
            if o == request.user:
                # get all the user's posts
                t = post.objects.filter(owner=o).order_by("-id")
                print(f"length of t,pe,ow = {len(t)}")
            # if he isn't the owner
            else:
                # filter for public posts from the page owne
                t = post.objects.filter(owner=o).filter(privacy = "pu")
                # check if the user follows the owner
                if o in request.user.follow.all():
                    # if he does, get the owner's followers only post too
                    f = post.objects.filter(owner=o).filter(privacy = "fo")
                    # than join all queries without dupplicates, ordering by the latest id,
                    t = t.union(f).order_by("-id")
                #else, just order the public posts by order
                else:
                    t = t.order_by("-id")
                print(f"length of t,pe,on = {len(t)}") 
                
                
        except:
            # if he is not logged
            # get the page's owner public posts only
            t = post.objects.filter(owner=o).filter(privacy = "pu").order_by("-id")
            print(f"length of t,pe,off = {len(t)}")

    # check how many posts we got for the set privacy
    length = len(t)
    print(f"length of data = {length}")
    # than how many pages that would give us
    # considering that each page can have up to 10 posts
    pages = length//10
    if length%10 != 0:
        pages = pages + 1
    print(f"pages = {pages}")

    # now check if the page requested is higher than 0 and
    # bellow or the same as the last page
    if page >= 1 and page<=pages:
        # to avoid errors, if the latest post is higher than the lenght
        # set the last to be equal to length (ex: page 2 so the latest
        # is post 20, but there are only 16 post, so now latest is 16)
        if last > length:
            last = length
        # limiting to between (first + 1) to last 
        t = t[first:last]

        # if selected page is higher than the max or below 1
    else:
        return JsonResponse({"error": "the selected page is beyond the scope"})

    # serialize the posts
    N=0
    for i in t:
        N=N+1
        # add the post to data
        # ps: serialize is a function created in models  
        data[f"post{N}"] = i.serialize(request.user)
        # append the posts "name" to n to be easier to go throught them
        n.append(f"post{N}")

    # add n to data as nu
    data["nu"]=n
    # add the current page and total pages to data 
    # for the pagination 
    data["page"] = page
    data["pages"] = pages

    # Return all the information to the page
    return JsonResponse(data)

#couldn't add csrf to everypost, so
@csrf_exempt
def like(request,id):
    # like/dislike must be via PUT
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."})
    # loads the information sent throught fetch
    data = json.loads(request.body)
    # get the posts id
    Post = post.objects.get(id=id) 
    # get the id of the user that (un)liked the post
    user=User.objects.get(id=data.get("User"))
    # check if the user already like/unlike the post
    # and change it's information in the database
    if data.get("like") =="like":
        Post.like.add(user)
    elif data.get("like") == "dislike":
        Post.like.remove(user)
    # if some information was sent wrong
    else:
        return JsonResponse({"error": "Not like nor dislike."})
    # if all good
    return JsonResponse({"OK": "All good"})

#loads the profile/personal page
def profile(request,id):
    p = User.objects.get(id=id)
    # ps: serialize is a function in models
    data = p.serialize(request.user)
    print(data)
    return JsonResponse(data)

# view to (un)follow users
@csrf_exempt
def follow(request,id,f):
    # get the page's owner information 
    p=User.objects.get(id=id)
    # check if the user is logged, more like a fail safe
    # and get his information
    try:
        d=User.objects.get(id=request.user.id)
    except:
        d = -1
        
    if request.method =="PUT":
        print(f"request = PUT")
        print(f"id = {id}")
        print(f"f = {f}")
        # add or remove the page owner from the user's follow list
        if f == "follow":
            d.follow.add(p)
        elif f == "unfollow":
            d.follow.remove(p)
    return JsonResponse({"worked": "All good"})

# view to reload specifics post
# used when un/like or edit a post
def getpost(request,id):

    # get the posts info
    o = post.objects.get(id=id)
    # check if the user is allowed to se this post
    try:
        if o.owner == request.user or o.privacy == "pu" or (request.user in o.owner.following.all() and o.privacy == "fo"):
            data=o.serialize(request.user)
        else:
            JsonResponse({"error": "You shouldn't be (here) seeing this post"})
    except:
            JsonResponse({"error": "Something went wrong"})
    return JsonResponse(data)

    

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
