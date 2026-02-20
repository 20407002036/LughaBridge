"""
URL routing for rooms API.
"""

from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('create/', views.create_room, name='create_room'),
    path('<str:room_code>/join/', views.join_room, name='join_room'),
    path('<str:room_code>/messages/', views.get_messages, name='get_messages'),
]
