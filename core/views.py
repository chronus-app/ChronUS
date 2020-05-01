from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, viewsets
from core.models import CollaborationRequest
from core.serializers import StudentSerializer, CollaborationRequestSerializer, CollaborationRequestOfferSerializer
from core.exceptions import ResourcePermissionException


class CreateStudentView(generics.CreateAPIView):
    """Create a new student in the system"""
    serializer_class = StudentSerializer
    permission_classes = []


class CollaborationRequestViewSet(mixins.CreateModelMixin,
                                  mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  viewsets.GenericViewSet):
    """Create a new collaboration request in the system"""
    serializer_class = CollaborationRequestSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """Filter the queryset depending on whether the parameter is applicant_id or offerer_id"""
        queryset = CollaborationRequest.objects.all()

        student = self.request.user.student
        
        applicant_id = self.request.query_params.get('applicant_id', None)
        if applicant_id is not None:
            if int(applicant_id) == student.user.id:
                queryset = queryset.filter(applicant=applicant_id)
            else:
                raise ResourcePermissionException()
        else:
            offerer_id = self.request.query_params.get('offerer_id', None)
            if offerer_id is not None:
                if int(offerer_id) == student.user.id:
                    queryset = queryset.filter(offerers=offerer_id)
                else: 
                    raise ResourcePermissionException()
        return queryset
    

class CollaborationRequestOfferView(generics.UpdateAPIView):
    """Add the current logged user to the collaboration request's offerers"""
    queryset = CollaborationRequest.objects.all()
    serializer_class = CollaborationRequestOfferSerializer
    lookup_field = 'id'
