from ..exceptions import UserSerializerNotFound
from .serializers import StudentUserSerializer, TeacherUserSerializer, UserSerializer


def get_serializer(user_type: str) -> UserSerializer:
    """Get the suitable serializer for user relying on its type

    This method uses a dictionary of serializers_classes to get the UserSerializer subclass
    that matches the given user type. If no serializer is found, it raises a UserSerializerNotFound exception.

    Args:
        user_type (str): the type of serializer

    Raises:
        UserSerializerNotFound: serializer not found error

    Returns:
        UserSerializer: serializer for register a user
    """

    # Define the serializers_classes dictionary
    serializers_classes = {
        "user": UserSerializer,
        "admin": UserSerializer,
        "teacher": TeacherUserSerializer,
        "student": StudentUserSerializer,
    }

    # Get the serializer from the dictionary
    serializer = serializers_classes.get(user_type, None)

    if not serializer:
        return UserSerializer

    # Return the serializer
    return serializer
