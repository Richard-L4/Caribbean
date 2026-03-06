from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('destinations/', views.destinations, name='destinations'),
    path('destinations-details/',
         views.destinations_details, name='destinations-details'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('confirm-logout/', views.confirm_logout, name='confirm-logout'),
    path('register/', views.register, name='register'),
]
