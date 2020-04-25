from django.urls import path
from core import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from core.serializers import AuthTokenSerializer

ObtainAuthToken.serializer_class = AuthTokenSerializer
ObtainAuthToken.renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
obtain_auth_token = ObtainAuthToken.as_view()

app_name = 'core'

urlpatterns = [
    path('students/', views.CreateStudentView.as_view(), name='create-student'),
    path('token/', obtain_auth_token),
]