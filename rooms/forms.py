from django import forms
from .models import Room, RoomAddress
from django_countries.widgets import CountrySelectWidget


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ["date_posted", "author", "favourite"]
        widgets = {
            'available_from': forms.widgets.DateInput(attrs={'type': 'date'})
        }


class UpdateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ["date_posted", "author", "favourite"]
        widgets = {
            'available_from': forms.widgets.DateInput(attrs={'type': 'date'})
        }


class LocationForm(forms.Form):
    city =forms.CharField(max_length=1024, required=False)
    distance = forms.IntegerField(label="Distance [km]", required=False)


class AddressForm(forms.ModelForm):
    class Meta:
        model = RoomAddress
        exclude = ['room', 'point']
        widgets = {'country': CountrySelectWidget()}

