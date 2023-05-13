from ..factories import UserTypeSerializerFactory


class KwargUserTypeSerializerMixin:
    def get_serializer_class(self):
        """
        Override method to get serializer_class depending on the url kwargs
        """

        # Get the serializer
        serializer_class = UserTypeSerializerFactory().get_suitable_serializer(
            self.kwargs["user_type"]
        )

        return serializer_class


class InUserTypeSerializerMixin:
    def get_serializer_class(self):
        """
        Override method to get serializer_class depending on the url kwargs
        """

        # Get the serializer
        serializer_class = UserTypeSerializerFactory().get_suitable_serializer(
            self.request.user.type.lower()
        )

        return serializer_class
