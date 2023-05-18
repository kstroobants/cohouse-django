from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Room, RoomImage
from .forms import CreateRoomForm, UpdateRoomForm
from .filters import RoomFilter


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
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['view_class'] = 'all'
        return context
    
    def get_queryset(self):
        queryset_temp = super().get_queryset()
        roomfilter = RoomFilter(self.request.GET, queryset=queryset_temp)
        self.form = roomfilter.form
        return roomfilter.qs
    
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


@login_required
def create_room(request):
    form = CreateRoomForm()
    images = []

    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        images = request.FILES.getlist('images')
        if form.is_valid():
            room = form.save(commit=False)
            room.author = request.user
            room.save()
            if len(images) == 0:
                RoomImage.objects.create(room=room)
            else:
                for i in images:
                    RoomImage.objects.create(room=room, image=i)
            return redirect("room-list")
    context = {'form':form}
    return render(request, 'rooms/room_form.html', context)


@login_required
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


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Room

    def get_success_url(self):
        return reverse_lazy( 'room-list')
    

    def test_func(self):
        room = self.get_object()
        if self.request.user == room.author:
            return True
        return False

