from rest_framework import serializers
from rest_framework.validators import ValidationError

from . import exceptions


class BaseSerializer(serializers.Serializer):
    """Inherited class from the base Serializer class"""

    def is_valid(self, *, raise_exception=False):
        """Override is_valid method to raise custom exceptions"""

        assert hasattr(self, "initial_data"), (
            "Cannot call `.is_valid()` as no `data=` keyword argument was "
            "passed when instantiating the serializer instance."
        )

        if not hasattr(self, "_validated_data"):
            try:
                self._validated_data = self.run_validation(self.initial_data)
            except ValidationError as exc:
                self._validated_data = {}
                self._errors = exc.detail
            else:
                self._errors = {}

        # Raise Field Error exception
        if self._errors and raise_exception:
            raise exceptions.SerializerFieldsError(errors=self.errors)

        return not bool(self._errors)
