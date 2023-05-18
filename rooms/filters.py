from . models import Room
import django_filters
from django_filters.filters import RangeFilter, ChoiceFilter, DateFromToRangeFilter
from django_filters.widgets import RangeWidget
from django import forms


class RoomFilter(django_filters.FilterSet):
    price = RangeFilter()
    size = RangeFilter()
    floor = RangeFilter()
    bathroom = RangeFilter()
    residents = RangeFilter()

    house_type = ChoiceFilter(choices=Room.House_type.choices)
    garden = ChoiceFilter(choices=Room.YesNo.choices)
    balcony = ChoiceFilter(choices=Room.YesNo.choices)
    parking = ChoiceFilter(choices=Room.YesNo.choices)
    furnished = ChoiceFilter(choices=Room.YesNo.choices)

    available_from = DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD'}))


    class Meta:
        model = Room
        exclude = ['author', 'description', 'date_posted']