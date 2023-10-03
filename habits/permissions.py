from rest_framework.permissions import BasePermission


class IsOwnerCRUD(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ['create', 'retrieve', 'update','destroy'] and request.user == obj.creator:
            return True
        return False

