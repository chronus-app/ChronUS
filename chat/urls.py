from django.urls import path

from . import views

urlpatterns = [
    path('messages/', views.ListMessagesView.as_view()),
    # path('<int:collaboration_id>/', views.room, name='room'),   
]
   