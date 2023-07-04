from cProfile import label

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import models, ModelForm, CheckboxSelectMultiple
from jsonschema._validators import required
from prompt_toolkit.widgets import Checkbox

from notatki.models import UserProfile, Note, Tag
from django import forms


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Login')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.form_method = 'POST'

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.form_method = 'POST'

class NoteForm(ModelForm):

    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
                                          widget=CheckboxSelectMultiple(),
                                          required=False
                                          )

    class Meta:
        model = Note
        fields = ['title', 'content', 'tags']

    def __init__(self, instance, *args, **kwargs):
        if instance:    # pobieranie wcześniej wybranych tagów
            initial = {'tags': instance.tag_set.all()}
            kwargs['initial'] = initial
        super().__init__(instance=instance, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.form_method = 'POST'

class NoteSearchForm(forms.Form):
    search_title = forms.CharField(max_length=200, required=False)
    search_text = forms.CharField(max_length=200, required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
                                          widget=forms.CheckboxSelectMultiple,
                                          required=False
                                          )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('search', 'Szukaj'))
        self.helper.form_method = 'POST'