"""
Views set for Books and Patron model api
"""
from rest_framework import viewsets
from rest_framework import permissions
from core.models import Patron, Book
from user.authentication import ExpiringTokenAuthentication
from . import serializers


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BookDetailSerializer
    queryset = Book.objects.all()
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.BookSerializer

        return self.serializer_class


class PatronViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PatronSerializer
    queryset = Book.objects.all()
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]



