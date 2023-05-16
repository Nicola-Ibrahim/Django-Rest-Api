from ..api import exceptions
from ..models.models import DeliveryWorker, Doctor, User, Warehouse


class UserTypeModelFactory:
    def get_suitable_model(self, type: str) -> User:  # type:ignore # noqa: A002
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
            "warehouse": Warehouse,
            "doctor": Doctor,
            "delivery_worker": DeliveryWorker,
        }
        model = models_classes.get(type, None)

        if not model:
            raise exceptions.UserModelNotFound()

        return model
