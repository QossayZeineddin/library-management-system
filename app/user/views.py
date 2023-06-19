"""
Views for the user API.
"""
from rest_framework.authtoken.models import Token
from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import (UserSerializer, AuthTokenSerializer)
from rest_framework.response import Response
from .authentication import ExpiringTokenAuthentication
import pytz
import datetime


class CreateUserView(generics.CreateAPIView):
    """Create new user in the system by api reqoust // this method handle the post request"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        utc_now = datetime.datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)
        Token.objects.filter(user=user, created__lt=utc_now - datetime.timedelta(seconds=60)).delete()
        Token.objects.get_or_create(user=user)
        return Response({
            'user_id': user.id,
            'email': user.email,
            'birthday': user.birthday,
            'token': user.auth_token.key,
        })


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """to manage data that come from authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
