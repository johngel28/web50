from django.shortcuts import render, redirect, get_object_or_404
from django import forms

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_content = util.get_entry(title)
    
    if entry_content is None:
        return render(request, "encyclopedia/404.html")

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": entry_content
    })

def search(request):
    query = request.GET.get('q', '')
    entries = util.list_entries()

    if query in entries:
        return redirect('entry', title=query)

    matching_entries = [entry for entry in entries if query.lower() in entry.lower()]

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "entries": matching_entries
    })

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

def new_page(request):
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if util.get_entry(title):
                return render(request, "encyclopedia/error.html", {
                    "error": "An entry with this title already exists."
                })

            util.save_entry(title, content)
            
            return redirect('entry', title=title)
    else:
        form = NewPageForm()

    return render(request, "encyclopedia/new.html", {
        "form": form
    })

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Content")

def edit_page(request, title):
    entry_content = util.get_entry(title)

    if entry_content is None:
        return render(request, "encyclopedia/404.html")

    if request.method == 'POST':
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]

            util.save_entry(title, content)
            
            return redirect('entry', title=title)
    else:
        form = EditPageForm(initial={'content': entry_content})

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": form
    })

import random

def random_page(request):
    entries = util.list_entries()
    if entries:
        random_entry = random.choice(entries)
        return redirect('entry', title=random_entry)
    else:
        return render(request, "encyclopedia/404.html")
