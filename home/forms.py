"""Custom forms for the public interface."""

from django import forms
from django.forms import ModelChoiceField, RadioSelect, ChoiceField, MultipleChoiceField
from crispy_forms.helper import FormHelper

from core.models import Poll


class CommentForm(forms.ModelForm):
    """A short form to submit comments."""
    pass # STUB_COMMENT

    """A form to vote on polls."""
    fields = ['options']
    widgets = {'options': MultipleChoiceField(choices=(("a", "A"), ("b", "B")))}
    helper = FormHelper()
    helper.form_tag = False
    helper.disable_csrf = True

    def __init__(self, poll, *args, **kwargs):
        super(PollVoteForm, self).__init__(*args, **kwargs)
        k = poll.options.split("SENTINEL")
        choices = zip(self.k, self.k)
        self.widgets = {'options':  MultipleChoiceField(
            choices=choices,
        )}
