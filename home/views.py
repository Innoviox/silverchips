"""The home view directory.

Contains the methods for normal news views. This app mainly consists
of everything a normal user would see while visiting the website.
"""

# Django imports
from django.shortcuts import render, get_object_or_404

# News imports
from core.models import Story, Image, Section


def load_context(request):
    return {"section_roots": Section.objects.all()}


def index(request):
    """Return the index page of the Silver Chips site."""

    return render(request, "home/index.html")


def view_section(request, name):
    """Render a section of the newspaper."""

    section = get_object_or_404(Section, name=name)

    return render(request, "home/section.html", {
        "section": section
    })


def read_story(request, pk):
    """Render a specific newspaper story."""

    story = get_object_or_404(Story, id=int(pk))

    story.views += 1
    story.save()
    
    return render(request, "home/story.html", {
        "story": story,
        "stories": Story.objects.all()
    })


def view_image(request, pk):
    """Render a specific newspaper image."""

    image = get_object_or_404(Image, id=int(pk))

    return render(request, "home/story.html", {
        "story": image,
        "stories": Story.objects.all()
    })
