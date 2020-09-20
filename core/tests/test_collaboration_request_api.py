from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Student, User, CollaborationRequest
from core.serializers import CollaborationRequestSerializer
import datetime


class PrivateCollaborationRequestApiTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            'test@test.com',
            'testpass1234'
        )
        self.student = Student.objects.create(user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(self.user)
    
    def test_retrieve_collaboration_requests(self):
        CollaborationRequest.objects.create(title='Ayuda en proyecto de inglés', requested_time=0.25, deadline=datetime.date(2021, 1, 1), applicant=self.student)
        CollaborationRequest.objects.create(title='Ayuda en proyecto de informática', requested_time=0.5, deadline=datetime.date(2021, 1, 5), applicant=self.student)

        res = self.client.get('/api/v1/collaboration-requests/')

        collaboration_requests = CollaborationRequest.objects.all()
        serializer = CollaborationRequestSerializer(collaboration_requests, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_create_collaboration_request(self):
        payload = {
            'title': 'Ayuda en proyecto de matemáticas',
            'requested_time': 1,
            'deadline': datetime.date(2021, 4, 2),
            'applicant': self.student
        }
        self.client.post('/api/v1/collaboration-requests/', payload)

        exists = CollaborationRequest.objects.filter(
            title=payload['title'],
            applicant=self.student
        ).exists()
        self.assertTrue(exists)