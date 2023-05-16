from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as users_views


urlpatterns = [
    path('register/', users_views.create_profile, name='create-profile'),
    path('profile/<int:pk>', users_views.show_profile, name='user-profile'),
    path('profile/update/', users_views.update_profile, name='update-profile'),
    path('profile/change-password/', users_views.change_password, name='change-password'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]