from django.shortcuts import render,redirect
from django.urls import reverse
from . import testingre
from . import util
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request,title):
    titles = util.list_entries()
    if title in titles:
        body=util.get_entry(title)
        body = testingre.read(body)
        return render(request, "encyclopedia/page.html",{
            "title":title, "body":body
    })
    else:
        return render(request, "encyclopedia/notF.html",{
            "title":title,
            })
def search(request):
    title=request.GET["q"]
    titles = util.list_entries()
    if title in titles:
        body=util.get_entry(title)
        body = testingre.read(body)
        return render(request, "encyclopedia/page.html",{
            "title":title, "body":body
        })
    else:
        results=[]
        for i in titles:
            if title.lower() in i.lower():
                results.append(i)
        return render(request, "encyclopedia/search.html", {
            "entries": results, "title":title
        })
def editEntry(request,title):

    if request.method=="GET":
        
        titles = util.list_entries()
        if title in titles:
            body=util.get_entry(title)
        return render(request, "encyclopedia/editEntry.html",{"title1":title,"oldTitle":title,"body":body,"error":""})

    if request.method == "POST":

        title=request.POST["title"]
        oldTitle=request.POST["oldTitle"]
        body=request.POST["content"]
        titles = util.list_entries()
        if title != oldTitle and title in titles:
            error="there is another wiki with this title"
            return render(request, "encyclopedia/newEntry.html",{"title1":title,"oldTitle":oldTitle,"body":body,"error":error})
        util.save_entry(title, body)
        return redirect("page",title=title)

def newEntry(request,title1="",body="",error=""):

    if request.method=="GET":
        return render(request, "encyclopedia/newEntry.html",{"title1":title1,"body":body,"error":error})

    if request.method == "POST":
        Title=request.POST["title"]
        body=request.POST["content"]
        #create a error
        titles = util.list_entries()
        if Title in titles:
            error="This wiki already exists"
            return render(request, "encyclopedia/newEntry.html",{"title1":Title,"body":body,"error":error})
        else:
            util.save_entry(Title, body)
            return redirect("page",title=Title)
def Random(request):
    titles = util.list_entries()
    ran=random.randint(0,len(titles)-1)
    title=titles[ran]
    body=util.get_entry(title)
    body = testingre.read(body)
    return render(request, "encyclopedia/page.html",{
            "title":title, "body":body
    })
