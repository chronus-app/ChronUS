from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Student
from core.models import User
import pdb

def create_student(**params):
    user = User.objects.create_user(**params)
    return Student.objects.create(user=user)
    
class PublicStudentApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'user': {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'johndoe@gmail.com',
                'password':  'testpassword'
            },
            'profile_image': '',
            'degrees': [
                {
                    'name': '0', 
                    'higher_grade': '3', 
                    'finished': False
                }
            ],
            'competences': [],
            'description': ''   
        }

    def test_create_valid_student_success(self):
        res = self.client.post('/api/v1/students/', self.payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        student = Student.objects.get(user=res.data['user']['id'])
        self.assertTrue(student.user.check_password(self.payload['user']['password']))

    def test_obtain_auth_token(self):
        create_student(**self.payload['user'])
        payload = {
            'email': self.payload['user']['email'],
            'password': self.payload['user']['password']
        }
        res = self.client.post('/api/v1/token/', payload)
        
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)