from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Room, RoomImage
from .forms import CreateRoomForm, UpdateRoomForm, AddressForm, LocationForm
from .filters import RoomFilter
import geocoder
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.contrib import messages
import folium


def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')
def values(request):
    return render(request, 'values.html')
def mission(request):
    return render(request, 'mission.html')
def story(request):
    return render(request, 'story.html')


class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    ordering = ['-date_posted']
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['location_form'] = LocationForm(self.request.GET)
        context['view_class'] = 'all'
        return context

    def get_queryset(self):
        queryset_temp = super().get_queryset()
        roomfilter = RoomFilter(self.request.GET, queryset=queryset_temp)
        self.form = roomfilter.form
        qs_new = roomfilter.qs

        if ('city' in self.request.GET) and ('distance' in self.request.GET):
            if (self.request.GET['distance'] != '') and (self.request.GET['distance'] != ''):
                radius = self.request.GET['distance']
                city_osm = geocoder.osm(self.request.GET['city'])
                if city_osm.ok == True:
                    city_point = Point(city_osm.latlng, srid=4326)
                    qs_new = qs_new.filter(roomaddress__point__distance_lte=(city_point, D(km=radius)))
                else:
                    messages.error(self.request, 'City in search not found!')

        return qs_new

    def post(self, request, *args, **kwargs):
        status = request.POST.get("favourite")
        status_like, room_id, redirect_url = status.split(",")
        room_obj = get_object_or_404(Room, id=room_id)

        if status_like == "favourite":
            room_obj.favourite.add(request.user)
        elif status_like == "unfavourite":
            room_obj.favourite.remove(request.user)

        return redirect(redirect_url)


class RoomUserListView(RoomListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_class'] = 'my'
        return context

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class RoomUserFavouriteListView(RoomListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_class'] = 'favourite'
        return context

    def get_queryset(self):
        return super().get_queryset().filter(favourite=self.request.user)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return redirect("room-favourite-list")


class RoomDetailView(LoginRequiredMixin, DetailView):
    model = Room

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        coords = context['object'].roomaddress.point.coords
        m = folium.Map(location=coords, zoom_start=13)
        folium.Marker(coords).add_to(m)
        context['map'] = m._repr_html_()
        return context


@login_required
def create_room(request):
    if request.method == 'POST':
        room_form = CreateRoomForm(request.POST)
        address_form = AddressForm(request.POST)
        images = request.FILES.getlist('images')
        if room_form.is_valid() and address_form.is_valid():
            room = room_form.save(commit=False)
            room.author = request.user

            address = address_form.save(commit=False)
            address_osm = geocoder.osm(", ".join((address_form.cleaned_data['address_line'], address_form.cleaned_data['zip_code'], address_form.cleaned_data['city'], address_form.cleaned_data['country'])))
            if address_osm.ok == True:
                address.point = Point(address_osm.latlng)
                room.save()
                address.room = room
                address.save()


                if len(images) == 0:
                    RoomImage.objects.create(room=room)
                else:
                    for i in images:
                        RoomImage.objects.create(room=room, image=i)
                return redirect("room-list")
            else:
                messages.error(request, 'Address not found!')
    else:
        room_form = CreateRoomForm()
        address_form = AddressForm()

    context = {'room_form':room_form, 'address_form':address_form}
    return render(request, 'rooms/room_form.html', context)


@login_required
def update_room(request, pk=None):
    room = get_object_or_404(Room, id=pk, author=request.user)
    if request.method == 'POST':
        room_form = UpdateRoomForm(request.POST, instance=room)
        address_form = AddressForm(request.POST, instance=room.roomaddress)
        images = request.FILES.getlist('images')
        del_imgs_id = request.POST.get("del_imgs")
        if room_form.is_valid() and address_form.is_valid():
            address = address_form.save(commit=False)
            address_osm = geocoder.osm(", ".join((address_form.cleaned_data['address_line'], address_form.cleaned_data['zip_code'], address_form.cleaned_data['city'], address_form.cleaned_data['country'])))
            if address_osm.ok == True:
                room = room_form.save()
                address.point = Point(address_osm.latlng)
                address.room = room
                address.save()

                # remove the default images when we add image/s
                if (len(images) > 0):
                    room.has_only_default(True)
                # add new images
                for i in images:
                    RoomImage.objects.create(room=room, image=i)
                # remove selected images
                if len(del_imgs_id) > 0:
                    del_imgs_id = del_imgs_id.split(",")
                    for img_id in del_imgs_id:
                        RoomImage.objects.filter(id=int(img_id)).delete()
                # add default if there are no images left
                if room.roomimage_set.count()==0:
                    RoomImage.objects.create(room=room)

                return redirect("room-detail", pk=pk)
            else:
                messages.error(request, 'Address not found!')
    else:
        room_form = UpdateRoomForm(None, instance=room)
        address_form = AddressForm(None, instance=room.roomaddress)

    context = {'room_form':room_form, 'address_form':address_form, 'room':room}
    return render(request, 'rooms/room_update.html', context)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Room

    def get_success_url(self):
        return reverse_lazy( 'room-list')


    def test_func(self):
        room = self.get_object()
        if self.request.user == room.author:
            return True
        return False

