from django.shortcuts import render

def content_page(request, content="home"):
  return render(request, "global_page.html", {"content":content})

