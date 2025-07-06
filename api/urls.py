from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('user/<str:username>', views.update_user_data, name='update_user_data'),
    path('users', views.get_all_users, name='get_all_users'),
]
