from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from .models import Room, RoomImage
from .forms import CreateRoomForm, UpdateRoomForm


def home(request):
    return render(request, 'home.html')


class RoomListView(ListView):
    model = Room
    ordering = ['-date_posted']


class RoomDetailView(DetailView):
    model = Room


def create_room(request):
    form = CreateRoomForm()
    images = []

    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        images = request.FILES.getlist('images')
        if form.is_valid():
            room = form.save()
            if len(images) == 0:
                RoomImage.objects.create(room=room)
            else:
                for i in images:
                    RoomImage.objects.create(room=room, image=i)
            return redirect("room-list")
    context = {'form':form}
    return render(request, 'rooms/room_form.html', context)


def update_room(request, pk=None):
    room = get_object_or_404(Room, id=pk, author=request.user)
    if request.method == 'POST':
        form = UpdateRoomForm(request.POST, instance=room)
        images = request.FILES.getlist('images')
        del_imgs_id = request.POST.get("del_imgs")
        if form.is_valid():
            room = form.save()
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
        form = UpdateRoomForm(None, instance=room)

    context = {'form':form, 'room':room}
    return render(request, 'rooms/room_update.html', context)


class PostDeleteView(DeleteView):
    model = Room
    success_url = 'room-list'

    def get_success_url(self):
        return reverse_lazy( 'room-list')

