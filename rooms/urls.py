from django.urls import path
from rooms import views as rooms_views


urlpatterns = [
    path('', rooms_views.RoomListView.as_view(), name='room-list'),
    path('user/', rooms_views.RoomUserListView.as_view(), name='room-user-list'),
    path('<int:pk>/', rooms_views.RoomDetailView.as_view(), name='room-detail'),
    path('new/', rooms_views.create_room, name='room-create'),
    path('<int:pk>/update/', rooms_views.update_room, name='room-update'),
    path('<int:pk>/delete/', rooms_views.PostDeleteView.as_view(), name='room-delete'),
]