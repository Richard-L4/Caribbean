from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('info/', views.info, name='info'),
    path('destinations/', views.destinations, name='destinations'),
    path('destinations-details/<int:pk>/',
         views.destinations_details, name='destinations-details'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('confirm-logout/', views.confirm_logout, name='confirm-logout'),
    path('register/', views.register, name='register'),
]
