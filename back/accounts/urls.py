from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.user_info),
    path('update/', views.update_account),
    path('delete/', views.delete_account),
    path('username/find/', views.find_username),
    path('password/reset/', views.reset_password),
    path('password/change/', views.change_password),
]