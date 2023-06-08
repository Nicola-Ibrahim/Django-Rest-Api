import django_filters.rest_framework as filters

from .. import exceptions
from .filters import StudentFilter, TeacherFilter, UserFilter


class UserTypeFilterFactory(filters.DjangoFilterBackend):
    """A factory class that returns the suitable filter class based on the user type.

    This class inherits from DjangoFilterBackend and overrides the get_filterset_class method
    to dynamically select the appropriate FilterSet subclass for filtering the queryset.

    Attributes:
        filters_classes (dict): A mapping of user types to their corresponding FilterSet subclasses.
    """

    filters_classes = {
        "user": UserFilter,
        "warehouse": TeacherFilter,
        "doctor": StudentFilter,
    }

    def get_suitable_filter(self, type: str) -> filters.FilterSet:
        """Returns the FilterSet subclass that matches the given user type.

        Args:
            type (str): The user type to filter by.

        Returns:
            filters.FilterSet: The FilterSet subclass that can filter the queryset by the user type.

        Raises:
            exceptions.UserFilterNotFound: If no FilterSet subclass is found for the given user type.
        """
        filter_ = self.filters_classes.get(type, None)

        if not filter_:
            raise exceptions.UserFilterNotFound()

        return filter_

    def get_filterset_class(self, view, queryset=None):
        """Return the `FilterSet` class used to filter the queryset.

        This method overrides the base class method and calls get_suitable_filter
        to get the FilterSet subclass based on the user type in the view kwargs.

        Args:
            view: The view instance that is requesting the filter.
            queryset: The queryset that is being filtered. Defaults to None.

        Returns:
            filters.FilterSet: The FilterSet subclass that can filter the queryset.

        Raises:
            AssertionError: If the FilterSet model does not match the queryset model.
        """
        # Get the FilterSet subclass from the user type
        # filterset_class = self.get_suitable_filter(view.kwargs["user_type"])
        filterset_class = self.get_suitable_filter(view.get("user_type", ""))

        # Get the fields to filter by from the view attribute
        filterset_fields = getattr(view, "filterset_fields", None)  # type: ignore # noqa: F841

        if filterset_class:
            # Get the model class from the FilterSet meta class
            filterset_model = filterset_class._meta.model  # type: ignore # noqa: E261

            # FilterSets do not need to specify a Meta class
            if filterset_model and queryset is not None:
                # Check that the queryset model is a subclass of the FilterSet model
                assert issubclass(
                    queryset.model, filterset_model
                ), "FilterSet model {} does not match queryset model {}".format(
                    filterset_model,
                    queryset.model,
                )

            return filterset_class
