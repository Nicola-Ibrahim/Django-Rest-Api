from . import serializers


def get_create_serializer(user_type: str) -> serializers.UserCreateSerializer:
    """Get the suitable serializer for user relying on its type

    This method uses a dictionary of serializers_classes to get the UserCreateSerializer subclass
    that matches the given user type. If no serializer is found, it raises a UserSerializerNotFound exception.

    Args:
        user_type (str): the type of serializer

    Raises:
        UserSerializerNotFound: serializer not found error

    Returns:
        UserCreateSerializer: serializer for register a user
    """

    serializers_classes = {
        "admin": serializers.AdminUserCreateSerializer,
        "teacher": serializers.TeacherUserCreateSerializer,
        "student": serializers.StudentUserCreateSerializer,
    }

    # Get the serializer from the serializers_classes dictionary
    serializer = serializers_classes.get(user_type.lower(), None)

    return serializer


def get_update_serializer(user_type: str) -> serializers.UserCreateSerializer:
    """Get the suitable serializer for user relying on its type

    This method uses a dictionary of serializers_classes to get the UserCreateSerializer subclass
    that matches the given user type. If no serializer is found, it raises a UserSerializerNotFound exception.

    Args:
        user_type (str): the type of serializer

    Raises:
        UserSerializerNotFound: serializer not found error

    Returns:
        UserCreateSerializer: serializer for register a user
    """

    serializers_classes = {
        "admin": serializers.AdminUserUpdateSerializer,
        "teacher": serializers.TeacherUserUpdateSerializer,
        "student": serializers.StudentUserUpdateSerializer,
    }

    # Get the serializer from the serializers_classes dictionary
    serializer = serializers_classes.get(user_type.lower(), None)

    return serializer
