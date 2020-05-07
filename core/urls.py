from django.urls import path, include
from core import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from core.serializers import AuthTokenSerializer
from rest_framework.routers import DefaultRouter

ObtainAuthToken.serializer_class = AuthTokenSerializer
ObtainAuthToken.renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
obtain_auth_token = ObtainAuthToken.as_view()

app_name = 'core'

router = DefaultRouter()
router.register(r'collaboration-requests', views.CollaborationRequestViewSet, basename='collaboration-requests')
router.register(r'collaborations', views.CollaborationViewSet, basename='collaborations')

urlpatterns = [
    path('students/', views.CreateStudentView.as_view(), name='create-student'),
    path('', include(router.urls)),
    path('collaboration-requests/<int:id>/offer/', views.CollaborationRequestOfferView.as_view(), name='offer-collaboration-request'),
    path('token/', obtain_auth_token),
    path('users/me/', views.RetrieveLoggedUserView.as_view({'get': 'retrieve'})),
    path('logout/', views.Logout.as_view())
]