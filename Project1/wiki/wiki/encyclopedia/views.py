from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request,title):
    titles = util.list_entries()
    if title in titles:
        body=util.get_entry(title)
        return render(request, "encyclopedia/page.html",{
            "title":title, "body":body
    })
    else:
        return render(request, "encyclopedia/notF.html",{
            "title":title,
            })
def search(request):
    print("test1")
    print(request)
    print("test2")
    title=request.GET["q"]
    titles = util.list_entries()
    if title in titles:
        body=util.get_entry(title)
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
        
