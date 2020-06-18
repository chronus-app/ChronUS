from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics
from chat.models import Message
from chat.serializers import MessageSerializer
from core.models import Collaboration
from core.exceptions import ResourcePermissionException


# def room(request, collaboration_id):
#     return render(request, 'chat/room.html', {
#         'collaboration_id': collaboration_id
#     })


class ListMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        student = self.request.user.student

        collaboration_id = self.request.query_params.get('collaboration_id', None)
        collaboration = get_object_or_404(Collaboration, id=collaboration_id)
        if collaboration.applicant == student or collaboration.collaborator == student:
            queryset = Message.objects.order_by('timestamp').filter(collaboration=collaboration_id)
            return queryset
        else:
            raise ResourcePermissionException
       