from django import forms 
from .models import Room


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ["date_posted"]
        widgets = {
            'available_from': forms.widgets.DateInput(attrs={'type': 'date'})
        }


class UpdateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ["date_posted", "author"]
        widgets = {
            'available_from': forms.widgets.DateInput(attrs={'type': 'date'})
        }

