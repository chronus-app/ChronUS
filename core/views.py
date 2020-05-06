from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, viewsets
from core.models import CollaborationRequest, Collaboration
from core.serializers import StudentSerializer, CollaborationRequestSerializer, CollaborationRequestOfferSerializer, CollaborationListSerializer, CollaborationRetrieveSerializer, CollaborationCreateSerializer
from core.exceptions import ResourcePermissionException


class CreateStudentView(generics.CreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = []


class CollaborationRequestViewSet(mixins.CreateModelMixin,
                                  mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin,
                                  viewsets.GenericViewSet):
    serializer_class = CollaborationRequestSerializer
    lookup_field = 'id'

    def get_queryset(self):
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
    queryset = CollaborationRequest.objects.all()
    serializer_class = CollaborationRequestOfferSerializer
    lookup_field = 'id'


class CollaborationViewSet(mixins.CreateModelMixin,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    
    def get_queryset(self):
        student = self.request.user.student

        return Collaboration.objects.filter(Q(applicant=student) | Q(collaborator=student))
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CollaborationListSerializer
        if self.action == 'retrieve':
            return CollaborationRetrieveSerializer
        if self.action == 'create':
            return CollaborationCreateSerializer

    def retrieve(self, request, *args, **kwargs):
        student = request.user.student
        collaboration = get_object_or_404(Collaboration, id=kwargs['pk'])
        if not student == collaboration.applicant and not student == collaboration.collaborator:
            raise ResourcePermissionException
        return super().retrieve(self, request, *args, **kwargs)    