from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Student, User, Collaboration, CollaborationRequest
from core.serializers import CollaborationListSerializer, CollaborationCreateSerializer
import datetime


class PrivateCollaborationApiTests(TestCase):

    def create_collaboration_request(self):
        collaboration_request = CollaborationRequest.objects.create(
            title='Ayuda en proyecto de matemáticas',
            requested_time=0.25, 
            deadline=datetime.date(2021, 1, 1), 
            applicant=self.applicant
        )
        collaboration_request.offerers.add(self.collaborator)

        return collaboration_request
        
    def setUp(self):
        self.applicant_user = User.objects.create_user(
            'applicant@test.com',
            'testpass1234'
        )
        self.collaborator_user = User.objects.create_user(
            'collaborator@test.com',
            'testpass4321'
        )
        self.applicant = Student.objects.create(user=self.applicant_user)
        self.collaborator = Student.objects.create(user=self.collaborator_user)

        self.collaboration_request = self.create_collaboration_request()

        self.client = APIClient()
        self.client.force_authenticate(self.applicant_user)
    
    def test_retrieve_collaborations(self):
        Collaboration.objects.create(
            title='Ayuda en proyecto de inglés',
             requested_time=0.25, 
             deadline=datetime.date(2021, 1, 1), 
             applicant=self.applicant, 
             collaborator=self.collaborator
        )
        Collaboration.objects.create(
            title='Ayuda en proyecto de física',
             requested_time=0.5, 
             deadline=datetime.date(2021, 1, 12), 
             applicant=self.applicant, 
             collaborator=self.collaborator
        )

        res = self.client.get('/api/v1/collaborations/')

        collaborations = Collaboration.objects.all()
        serializer = CollaborationListSerializer(collaborations, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_create_collaboration(self):
        payload = {
            'collaborator_id': self.collaborator.user.id,
            'collaboration_request': self.collaboration_request.id
        }

        self.client.post('/api/v1/collaborations/', payload)

        exists = Collaboration.objects.filter(
            title=self.collaboration_request.title,
            applicant=self.applicant
        ).exists()
        self.assertTrue(exists)