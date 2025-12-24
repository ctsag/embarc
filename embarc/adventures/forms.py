from django.forms import CheckboxInput, ModelForm, Select, TextInput, Textarea, HiddenInput
from adventures.models import Adventure, Mission


class AdventureForm(ModelForm):
    class Meta:
        model = Adventure
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'size': 64, 'autofocus': True}),
            'description': Textarea(attrs={'size': 512})
        }


class MissionForm(ModelForm):
    class Meta:
        model = Mission
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'size': 64, 'autofocus': True}),
            'notes': Textarea(attrs={'size': 512}),
            'completed': Select(),
            'adventure': HiddenInput,
            'parent': HiddenInput
        }
