from django.urls import path

from chat import consumers

websocket_urlpatterns = [
    path('ws/collaborations/<int:collaboration_id>/', consumers.ChatConsumer),
]