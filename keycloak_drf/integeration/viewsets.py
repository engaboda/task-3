from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsAdminUser, IsNormalUser


class AdminViewSet(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    @staticmethod
    def get(request, *args, **kwargs):
        return Response({'status': request.user.role})


class NomrlaViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsNormalUser | IsAdminUser]

    @staticmethod
    def get(request, *args, **kwargs):
        return Response({'status': request.user.role})
