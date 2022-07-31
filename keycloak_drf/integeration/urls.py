from integeration.jwt_views import KeycloakTokenObtainPairView
from django.urls import path
from .import viewsets


urlpatterns = [
    path('token/', KeycloakTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('normal/', viewsets.NomrlaViewSet.as_view(), name='normal'),
    path('admin/', viewsets.AdminViewSet.as_view(), name='admin')
]
