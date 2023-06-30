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

    serializers_classes = {
        "user": UserSerializer,
        "admin": UserSerializer,
        "teacher": TeacherUserSerializer,
        "student": StudentUserSerializer,
    }

    # Get the serializer from the serializers_classes dictionary
    print(user_type)
    serializer = serializers_classes.get(user_type, UserSerializer)

    return serializer
