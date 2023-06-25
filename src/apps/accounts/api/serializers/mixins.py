from ..serializers.serializers import UserSerializer
from .factories import get_suitable_serializer


class QueryParamUserTypeSerializerMixin:
    def get_serializer_class(self):
        """
        Override method to get serializer_class depending on the url kwargs
        """

        print(self.request.method)
        if self.request.method == "GET":
            return UserSerializer

        if self.request.method == "POST":
            serializer_class = get_suitable_serializer(self.request.query_params.get("user_type"))
            return serializer_class


class InUserTypeSerializerMixin:
    def get_serializer_class(self):
        """
        Override method to get serializer_class depending on the url kwargs
        """

        # Get the serializer
        serializer_class = get_suitable_serializer(self.request.user.type.lower())

        return serializer_class
