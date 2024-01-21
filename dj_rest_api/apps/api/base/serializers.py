import datetime

from rest_framework import serializers
from rest_framework.validators import ValidationError

from . import exceptions


class BaseModelSerializer(serializers.ModelSerializer):
    """Inherited class from the Model Serializer class"""

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
            raise exceptions.SerializerFieldsAPIException(errors=self._errors)

        return not bool(self._errors)


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
            raise exceptions.SerializerFieldsAPIException(errors=self.errors)

        return not bool(self._errors)


class HourTimeField(serializers.TimeField):
    # Use a custom format for the output representation of the time
    format = "%H:00:00"

    def to_internal_value(self, value):
        # Parse the input string with only hours
        try:
            hour = int(value)
        except ValueError:
            raise serializers.ValidationError("Invalid time format. Expected only hours.")

        # Check if the hour is valid
        if hour < 0 or hour > 23:
            raise serializers.ValidationError("Invalid hour value. Expected between 0 and 23.")

        # Convert the hour to a datetime.time object
        return datetime.time(hour=hour)
