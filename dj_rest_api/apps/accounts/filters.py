import django_filters.rest_framework as filters
from apps.accounts.models import User


class UserFilter(filters.FilterSet):
    """A FilterSet subclass for filtering User model instances.

    This class defines the fields and lookup expressions that can be used to filter
    the User queryset by email and verification status.

    Attributes:
        Meta: A class that contains the model and fields information for the FilterSet.
    """

    class Meta:
        model = User
        fields = {
            "email": ["icontains"],
            "is_verified": ["exact"],
        }
