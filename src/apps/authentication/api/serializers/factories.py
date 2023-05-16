from ..exceptions import UserSerializerNotFound
from .serializers import DeliveryWorkerUserSerializer, DoctorUserSerializer, UserSerializer, WarehouseUserSerializer


class UserTypeSerializerFactory:
    """A factory class that returns the suitable serializer class based on the user type.

    This class defines a method that takes a user type as an argument and returns the corresponding
    UserSerializer subclass for registering a user of that type.

    Attributes:
        serializers_classes (dict): A mapping of user types to their corresponding UserSerializer subclasses.
    """

    def get_suitable_serializer(self, type: str) -> UserSerializer:
        """Get the suitable serializer for user relying on its type

        This method uses a dictionary of serializers_classes to get the UserSerializer subclass
        that matches the given user type. If no serializer is found, it raises a UserSerializerNotFound exception.

        Args:
            type (str): the type of serializer

        Raises:
            UserSerializerNotFound: serializer not found error

        Returns:
            UserSerializer: serializer for register a user
        """

        # Define the serializers_classes dictionary
        serializers_classes = {
            "user": UserSerializer,
            "admin": UserSerializer,
            "warehouse": WarehouseUserSerializer,
            "doctor": DoctorUserSerializer,
            "delivery_worker": DeliveryWorkerUserSerializer,
        }

        # Get the serializer from the dictionary
        serializer = serializers_classes.get(type, None)

        # Raise an exception if no serializer is found
        if not serializer:
            raise UserSerializerNotFound()

        # Return the serializer
        return serializer
