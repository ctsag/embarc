from django.forms import CheckboxInput, ModelForm, Select, TextInput
from adventures.models import Adventure, Mission


class AdventureForm(ModelForm):
    class Meta:
        model = Adventure
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'size': 64, 'autofocus': True}),
            'description': TextInput(attrs={'size': 64})
        }


class MissionForm(ModelForm):
    class Meta:
        model = Mission
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'size': 64, 'autofocus': True}),
            'notes': TextInput(attrs={'size': 64}),
            'completed': CheckboxInput(),
            'adventure': Select(),
            'parent': Select()
        }
