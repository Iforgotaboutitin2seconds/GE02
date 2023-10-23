from django.forms import ModelForm
from .models import Project
from django import forms
# create class for project form


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'description')

class DeleteProjectForm(forms.Form):
    confirmation = forms.BooleanField(help_text="Check this box to confirm deletion", required=True)
