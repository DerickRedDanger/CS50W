from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from . import forms
from django.contrib.auth.decorators import login_required
import time
def index(request):
    ##return HttpResponse("works")
    return render(request, "test/index.html")

#Single plage - start 
texts=["Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua",
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. ",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",]

def section(request,num):
    if 1<= num <= 4:
        return HttpResponse(texts[num-1])
    else:
        raise Http404('No such section')
#Single plage - end

def reindex(request):
    ##return HttpResponse("works")
    return render(request, "test/reindex.html")

def posts(request):
    # Get start and end points
    start =int(request.GET.get("start") or 0)
    end = int (request.GET.get("end") or (start + 19))

    # Generate list of posts
    data = []
    for i in range(start, end + 1 ):
        data.append(f"Post #{i}")
    data2={"post":data}

    # Arttificially delay speed of response
    time.sleep(1)

    # Return list of post
    return JsonResponse(data2)

