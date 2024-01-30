from core.api.permissions import BasePermission

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class UserListCreatePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":  # give full access for `POST` request
            return True

        return super().has_permission(request, view)  # for others, check user against permissions


class UserDetailsUpdateDestroyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.method == "DELETE":
            # Users can only delete their own account
            return user == obj

        if request.method in ["PUT", "PATCH"]:
            # Users can only update their own account
            return user == obj

        return super().has_object_permission(request, view, obj)
