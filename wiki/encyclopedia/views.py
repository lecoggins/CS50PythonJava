from django.shortcuts import render
from markdown2 import Markdown
from . import util

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html",{
            "message": "This entry does not exist"
            })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    
def search(request):
    if request.method == "POST":
        entry_search = request.POST["q"]
        html_content = convert_md_to_html(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
        })
        else:
            entries = util.list_entries()
            results = []
            for entry in entries:
                if entry_search.lower() in entry.lower():
                    results.append(entry)
            return render(request, "encyclopedia/search.html", {
                "title": entry_search,
                "results": results
        })

def newpage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html",)
    else:
        title=request.POST['new_title']
        title_exists = util.get_entry(title)
        if title_exists is not None:
            return render(request, "encyclopedia/error.html",{
                "message": "This entry already exists"
            })
        else:
            content=request.POST['content']
            util.save_entry(title, content)
            html_content = convert_md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
         })
            
