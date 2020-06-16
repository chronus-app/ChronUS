from django.urls import path

from . import views

urlpatterns = [
    path('messages/', views.ListMessagesView.as_view()),
]
   