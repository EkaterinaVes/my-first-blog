from rest_framework.permissions import BasePermission
from .models import Post

class IsAuthor(BasePermission):
    """Custom permission class to allow only tasklist owners to edit them."""

    def has_object_permission(self, request, view, obj):
        """Return True if permission is granted to the bucketlist owner."""
        if isinstance(obj, Post):
            return obj.author == request.user
        return obj.author == request.user