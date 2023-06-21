from core.models import Book, Patron
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    """Serializer for book."""
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publication_date']
        read_only_fields = ['id']


class BookDetailSerializer(BookSerializer):
    """Serializer for book detail view."""

    class Meta(BookSerializer.Meta):
        model = BookSerializer.Meta.model
        fields = BookSerializer.Meta.fields + ['created_at', 'updated_at', 'price']


class PatronSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patron
        fields = ['id', 'name', 'email', 'birthday', 'created_at', 'updated_at']
