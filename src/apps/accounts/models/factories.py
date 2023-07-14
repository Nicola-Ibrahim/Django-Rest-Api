from ..api import exceptions
from ..models.models import Student, Teacher, User


def get_model(user_type: str) -> User:  # type:ignore # noqa: A002
    """Get the suitable serializer for user relying on its type

    Args:
        type (str): the type of model

    Raises:
        UserModelNotFound: model not found error

    Returns:
        User: model for register a user
    """

    models_classes = {
        "user": User,
        "admin": User,
        "warehouse": Teacher,
        "doctor": Student,
    }
    model = models_classes.get(user_type, User)

    return model
