"""Custom forms for the public interface."""

from django import forms
from django.forms import ModelChoiceField, RadioSelect
from crispy_forms.helper import FormHelper

from core.models import Poll


class CommentForm(forms.ModelForm):
    """A short form to submit comments."""
    pass # STUB_COMMENT

class PollVoteForm(forms.ModelForm):
    """A form to vote on polls."""
    def __init__(self, poll, *args, **kwargs):
        super(PollVoteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

        self.widgets = {'options': ModelChoiceField(
            label='Options',
            queryset=poll.options.split("SENTINEL"),
            widget=RadioSelect,
            required=True,
            empty_label=None,
            initial=None,
        )}

    class Meta:
        model = Poll
        fields = ['options']

        def __init__(self, poll, *args, **kwargs):
            super().__init__(*args, **kwargs)
