from src.apps.accounts.models import factories as model_factories


class QueryParamUserTypeQuerySetMixin:
    """A mixin class that provides a get_queryset method based on the user type in the view kwargs.

    This class assumes that the view has a user_type attribute in its kwargs dictionary,
    and uses the UserTypeModelFactory to get the suitable model class for that user type.
    Then, it returns a queryset of all instances of that model class.

    Attributes:
        kwargs (dict): A dictionary of keyword arguments passed to the view.
    """

    def get_queryset(self):
        """Returns a queryset of model instances based on the user type in the view kwargs.

        Returns:
            QuerySet: A queryset of model instances that match the user type.
        """

        # Get the model
        model = model_factories.get_model(user_type=self.request.GET.get("user_type"))
        queryset = model.objects.all()
        return queryset


class InUserTypeQuerySetMixin:
    """A mixin class that provides a get_queryset method based on the user type in the request.

    This class assumes that the request has a user attribute with a type attribute,
    and uses the UserTypeModelFactory to get the suitable model class for that user type.
    Then, it returns a queryset of all instances of that model class.

    Attributes:
        request: The request object passed to the view.
    """

    def get_queryset(self):
        """Returns a queryset of model instances based on the user type in the request.

        Returns:
            QuerySet: A queryset of model instances that match the user type.
        """

        # Get the model
        model = model_factories.get_model(self.request.user.type.lower())
        queryset = model.objects.all()
        return queryset
