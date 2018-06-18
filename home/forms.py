"""Custom forms for the public interface."""

from django import forms
from django.forms import ModelChoiceField, RadioSelect
from crispy_forms.helper import FormHelper


class CommentForm(forms.ModelForm):
    """A short form to submit comments."""
    pass # STUB_COMMENT

class PollVoteForm(forms.ModelForm):
    """A form to vote on polls."""

    def __init__(self, *args, poll, **kwargs):
        super(PollVoteForm, self).__init__(*args, **kwargs)
        self.poll = poll
        self.helper = FormHelper()

        self.fields['choice'] = ModelChoiceField(
            label='Options',
            queryset=poll.options.split("SENTINEL"),
            widget=RadioSelect,
            required=True,
            empty_label=None,
            initial=None,
        )

    def make_choice(self, user):
        choice = self.cleaned_data['choice']
        self.poll.vote(user.person, choice)