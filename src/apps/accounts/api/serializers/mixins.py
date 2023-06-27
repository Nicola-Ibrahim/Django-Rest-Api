from ..serializers.serializers import UserSerializer
from . import factories as serializer_factory


class QueryParamUserTypeSerializerMixin:
    def get_serializer_class(self):
        """
        Get the appropriate serializer depending on the url user_type param
        """

        if self.request.method == "POST":
            serializer_class = serializer_factory.get_serializer(self.request.GET.get("user_type"))
            return serializer_class


class InUserTypeSerializerMixin:
    def get_serializer_class(self):
        """
        Override method to get serializer_class depending on the url kwargs
        """

        # Get the serializer
        serializer_class = serializer_factory.get_serializer(self.request.user.type.lower())

        return serializer_class
