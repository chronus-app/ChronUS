from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import CollaborationRequest, Collaboration, Student, Competence
from core.serializers import (StudentSerializer, CollaborationRequestSerializer, 
CollaborationRequestOfferSerializer, CollaborationListSerializer, 
CollaborationRetrieveSerializer, CollaborationCreateSerializer, CompetenceSerializer)
from core.exceptions import ResourcePermissionException
from datetime import date

class CreateStudentView(generics.CreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = []


class RetrieveLoggedStudentView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_object(self):
        return self.request.user.student


class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class CollaborationRequestViewSet(mixins.CreateModelMixin,
                                  mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin,
                                  viewsets.GenericViewSet):
    serializer_class = CollaborationRequestSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = CollaborationRequest.objects.filter(deadline__gte=date.today())

        student = self.request.user.student
        
        applicant_id = self.request.query_params.get('applicant_id', None)
        if applicant_id is not None:
            if int(applicant_id) == student.user.id:
                queryset = queryset.filter(applicant=applicant_id, deadline__gte=date.today())
            else:
                raise ResourcePermissionException()
        else:
            offerer_id = self.request.query_params.get('offerer_id', None)
            if offerer_id is not None:
                if int(offerer_id) == student.user.id:
                    queryset = queryset.filter(offerers=offerer_id, deadline__gte=date.today())
                else: 
                    raise ResourcePermissionException()
        return queryset

    def retrieve(self, request, *args, **kwargs):
        collaboration_request = get_object_or_404(CollaborationRequest, id=kwargs['id'])
        if collaboration_request.deadline < date.today():
            raise ResourcePermissionException('This collaboration request has expired')
        return super().retrieve(self, request, *args, **kwargs)
    

class CollaborationRequestOfferView(generics.UpdateAPIView):
    queryset = CollaborationRequest.objects.all()
    serializer_class = CollaborationRequestOfferSerializer
    lookup_field = 'id'


class CollaborationViewSet(mixins.CreateModelMixin,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    lookup_field = 'id'

    def get_queryset(self):
        student = self.request.user.student

        return Collaboration.objects.filter(Q(applicant=student) | Q(collaborator=student)).filter(deadline__gte=date.today())
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CollaborationListSerializer
        if self.action == 'retrieve':
            return CollaborationRetrieveSerializer
        if self.action == 'create':
            return CollaborationCreateSerializer

    def retrieve(self, request, *args, **kwargs):
        student = request.user.student
        collaboration = get_object_or_404(Collaboration, id=kwargs['id'])
        if not student == collaboration.applicant and not student == collaboration.collaborator:
            raise ResourcePermissionExceptionç
        if collaboration.deadline < date.today():
            raise ResourcePermissionException('This collaboration has expired')
        return super().retrieve(self, request, *args, **kwargs)


class ListCompetencesView(generics.ListAPIView):
    serializer_class = CompetenceSerializer
    queryset = Competence.objects.all()
    permission_classes = []