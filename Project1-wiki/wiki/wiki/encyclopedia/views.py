from django.shortcuts import render,redirect
from django.urls import reverse
from . import testingre
from . import util
import random

#index view
def index(request):
    #returns all entries
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
#page for each entry in the wiki
def page(request,title):
    #gets all titles
    titles = util.list_entries()
    #if the given title is inside the titles list
    if title in titles:
        #get the information from the entry
        body=util.get_entry(title)
        #translate that information into html code
        body = testingre.read(body)
        #return the title's page
        return render(request, "encyclopedia/page.html",{
            "title":title, "body":body
    })
    else:
        #else, return that it's not in the database
        return render(request, "encyclopedia/notF.html",{
            "title":title,
            })
#page for the search function  
def search(request):
    #get the input to be searched
    title=request.GET["q"]
    titles = util.list_entries()
    #if that input is in the entry list
    if title in titles:
        body=util.get_entry(title)
        body = testingre.read(body)
        #return that entry's page
        return render(request, "encyclopedia/page.html",{
            "title":title, "body":body
        })
    else:
        #else, create a empty list
        results=[]
        #look for titles that have that input in it
        for i in titles:
            if title.lower() in i.lower():
                #append them to the list
                results.append(i)
        #return theses titles
        return render(request, "encyclopedia/search.html", {
            "entries": results, "title":title
        })
#page to edit entries
def editEntry(request,title):

    if request.method=="GET":
        #if arrived here throught get
        titles = util.list_entries()
        #check if the title is in the entry list
        if title in titles:
            #shows the edit page of the requested title 
            body=util.get_entry(title)
        return render(request, "encyclopedia/editEntry.html",{"title1":title,"oldTitle":title,"body":body,"error":""})

    if request.method == "POST":
        #if throught post, get the information from the page
        title=request.POST["title"]
        oldTitle=request.POST["oldTitle"]
        body=request.POST["content"]
        titles = util.list_entries()
        #check if the user changed the title and if the new title is alrady in use
        if title != oldTitle and title in titles:
            #warn if either returns true
            error="there is another wiki with this title"
            return render(request, "encyclopedia/newEntry.html",{"title1":title,"oldTitle":oldTitle,"body":body,"error":error})
        #save the information otherwise
        util.save_entry(title, body)
        return redirect("page",title=title)
#page for new entries
def newEntry(request,title1="",body="",error=""):
    
    if request.method=="GET":
        #if through get, show the newnetry page
        return render(request, "encyclopedia/newEntry.html",{"title1":title1,"body":body,"error":error})

    if request.method == "POST":
        # if post
        Title=request.POST["title"]
        body=request.POST["content"]
        titles = util.list_entries()
        # check if the title already exist
        if Title in titles:
            #return error if it does
            error="This wiki already exists"
            return render(request, "encyclopedia/newEntry.html",{"title1":Title,"body":body,"error":error})
        else: 
            #save otherwise
            util.save_entry(Title, body)
            return redirect("page",title=Title)
#page for the random page function
def Random(request):
    #get all titles
    titles = util.list_entries()
    #get one at random from the list
    ran=random.randint(0,len(titles)-1)
    title=titles[ran]
    #show this title's page
    body=util.get_entry(title)
    body = testingre.read(body)
    return render(request, "encyclopedia/page.html",{
            "title":title, "body":body
    })
