"""Custom forms for the public interface."""

from django import forms
from django.forms import ChoiceField


class CommentForm(forms.ModelForm):
    """A short form to submit comments."""
    pass # STUB_COMMENT

def PollVoteForm(poll):
    choices = poll.options.split("SENTINEL")
    class _Form(forms.Form):
        choice = ChoiceField(choices=enumerate(choices))
    return _Form