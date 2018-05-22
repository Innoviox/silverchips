"""The staff view map.

Handles the side of the site for writers, editors, and managers.
Also allows for some degree of customization.
"""


# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import CreateView, UpdateView, View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q

# Local imports
from core import models
from core.permissions import can, VISIBILITY_ACTIONS, UserCanMixin, user_can
from staff import forms


# Staff views
def login(request):
    """Login to the staff site."""
    # Redirect users who are already authenticated
    if request.user.is_authenticated:
        return redirect("staff:index")

    # Check for login form submission
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # Attempt to authenticate the user
            user = auth.authenticate(username=form.cleaned_data["username"],
                                     password=form.cleaned_data["password"])

            # Check if password wrong
            if not user:
                form.add_error(None, "Invalid credentials")

            # Check if user is inactive
            elif not user.is_active:
                form.add_error(None, "User is inactive")

            # Login and redirect to staff
            else:
                auth.login(request, user)
                return redirect("staff:index")

    else:
        form = forms.LoginForm()

    return render(request, "staff/login.html", {"form": form})


@login_required
def logout(request):
    """Log out the user and go to logout page."""
    auth.logout(request)
    return redirect("staff:index")


@login_required
def index(request):
    """Return the staff dashboard page."""
    return render(request, "staff/index.html")


class EditorMixin(View):
    """Simple mixin that allows various forms to use our generic editor template instead of using separate templates."""
    template_name = "staff/editor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editing'] = self.editing
        return context


# Content views
class ContentListView(LoginRequiredMixin, ListView):
    """The content list view that supports pagination."""

    template_name = "staff/content/list.html"
    context_object_name = "content_list"
    paginate_by = 25

    def get_queryset(self):
        """Return a list of all the content we're looking at, filtered by search criteria."""
        if self.request.user.has_perm('core.read_content'):
            content = models.Content.objects.all()
        else:
            content = models.Content.objects.filter(authors=self.request.user).all()

        form = forms.ContentSearchForm(self.request.GET)

        if form.is_valid():
            # Filter the content by certain criteria
            query = Q()

            if form.data.get("title"):
                query &= Q(title__contains=form.data['title'])
            if form.data.get("id"):
                query &= Q(pk=int(form.data['id']))
            if form.data.get("after"):
                query &= Q(created__gt=form.data['after'])
            if form.data.get("before"):
                query &= Q(created__lt=form.data['before'])
            if form.data.get("authors"):
                query &= Q(authors=form.data['authors'])

            content = content.filter(query)

        return content.order_by('-modified')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.ContentSearchForm(self.request.GET)
        return context


class ContentChangeMixin(LoginRequiredMixin):
    """Mixin that organizes shared functionality across various content creation and editing views."""
    def get_success_url(self):
        return reverse("staff:content:list")

    def form_valid(self, form):
        # Automatically update the "modified" field when the form is saved
        form.instance.modified = timezone.now()
        return super().form_valid(form)


class ContentCreateView(ContentChangeMixin, PermissionRequiredMixin, EditorMixin, CreateView):
    """Base view for uploading new content."""
    permission_required = 'core.create_content'

    def get_initial(self):
        return dict(super(ContentCreateView, self).get_initial(), authors=[self.request.user])


class StoryCreateView(ContentCreateView):
    """View for uploading a new story."""
    model = models.Story
    form_class = forms.StoryForm
    editing = "Story"


class ImageCreateView(ContentCreateView):
    """View for uploading a new image."""
    model = models.Image
    form_class = forms.ImageForm
    editing = "Image"


class VideoCreateView(ContentCreateView):
    """View for uploading a new video."""
    model = models.Video
    form_class = forms.VideoForm
    editing = "Video"


class AudioCreateView(ContentCreateView):
    """View for uploading new audio."""
    model = models.Audio
    form_class = forms.AudioForm
    editing = "Audio"


class PollCreateView(ContentCreateView):
    """View for uploading a new poll."""
    pass # STUB_POLL


class ContentEditView(ContentChangeMixin, UserCanMixin, EditorMixin, UpdateView):
    """Base view for editing content."""
    action = 'content.edit'


class StoryEditView(ContentEditView):
    """View for editing stories."""
    model = models.Story
    form_class = forms.StoryForm
    editing = "Story"

class ImageEditView(ContentEditView):
    """View for editing images."""
    model = models.Image
    form_class = forms.ImageForm
    editing = "Image"


class VideoEditView(ContentEditView):
    """View for editing videos."""
    model = models.Video
    form_class = forms.VideoForm
    editing = "Video"


class AudioEditView(ContentEditView):
    """View for editing audio."""
    model = models.Audio
    form_class = forms.AudioForm
    editing = "Audio"


class PollEditView(ContentEditView):
    """View for editing polls."""
    pass # STUB_POLL


def content_edit_view(request, pk):
    """View for editing general content, rendering different views depending on the type of content."""
    content = get_object_or_404(models.Content.objects, pk=pk)

    # Switch which view gets received based on the kind of content
    return {
        'Story': StoryEditView,
        'Image': ImageEditView,
        'Video': VideoEditView,
        'Audio': AudioEditView,
        'Poll': PollEditView
    }[content.type].as_view()(request, pk=pk)


@login_required
@csrf_protect
@require_http_methods(["PATCH"])
def set_content_visibility(request, pk, level):
    """View to change the visibility of certain content."""
    content = get_object_or_404(models.Content.objects, pk=pk)

    # Check whether the requesting user has permission to change the content's visibility to the given level
    if not can(request.user, VISIBILITY_ACTIONS[level], content):
        raise PermissionDenied

    content.visibility = level
    content.save()

    return HttpResponse(status=200)


@login_required
@csrf_protect
@user_can('content.delete')
@require_http_methods(["DELETE"])
def delete_content(request, pk):
    """View to delete content."""
    content = get_object_or_404(models.Content.objects, pk=pk)
    content.delete()

    return HttpResponse(status=200)


# User views
class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """The content list view that supports pagination."""
    permission_required = 'auth.manage_users'

    template_name = "staff/users/list.html"
    context_object_name = "user_list"
    paginate_by = 25

    def get_queryset(self):
        """Return a list of all the users we're looking at, filtered by search criteria."""
        users = models.User.objects.all()

        form = forms.UserSearchForm(self.request.GET)
        if form.is_valid():
            # Filter the users by certain criteria
            query = Q()

            if 'id' in form.data and form.data['id']:
                query &= Q(pk=int(form.data['id']))
            if 'first_name' in form.data and form.data['first_name']:
                query &= Q(first_name__contains=form.data['first_name'])
            if 'last_name' in form.data and form.data['last_name']:
                query &= Q(last_name__contains=form.data['last_name'])
            if 'graduation_year' in form.data and form.data['graduation_year']:
                query &= Q(profile__graduation_year=form.data['graduation_year'])
            # if 'active' in form.data and form.data['active']:
            #     query &= Q(active=form.data['active'])

            users = users.filter(query)

        return users

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.UserSearchForm(self.request.GET)
        return context



class UserChangeMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'auth.manage_users'

    # def form_valid(self):


class UserCreateView(UserChangeMixin, CreateView):
    """Base view for creating users."""

    editing = "User"


class UserManageView(UserChangeMixin, UpdateView):
    """Base view for editing users."""

    model = models.User
    form_class = forms.UserForm
    editing = "User"


class ProfileEditView(LoginRequiredMixin, UserCanMixin, EditorMixin, UpdateView):
    """Base view for editing user profiles."""
    action = 'users.edit_profile'

    model = models.Profile
    form_class = forms.ProfileForm
    editing = "Profile"


# Comment views
class CommentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    pass # STUB_COMMENT


@login_required
@csrf_protect
@permission_required("") # STUB_COMMENT
@require_http_methods(["PATCH"])
def approve_content(request, pk, approved):
    pass # STUB_COMMENT