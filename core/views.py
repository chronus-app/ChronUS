from rest_framework import generics 
from core.serializers import StudentSerializer


class CreateStudentView(generics.CreateAPIView):
    """Create a new student in the system"""
    serializer_class = StudentSerializer
    permission_classes = []
