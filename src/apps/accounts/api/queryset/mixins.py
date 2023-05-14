from ..factories import UserTypeModelFactory


class KwargUserTypeQuerySetMixin:
    def get_queryset(self):
        """
        Override method to get queryset depending on the url kwargs
        """

        # Get the model
        model = UserTypeModelFactory().get_suitable_model(
            self.kwargs["user_type"]
        )
        queryset = model.objects.all()
        return queryset


class InUserTypeQuerySetMixin:
    def get_queryset(self):
        """
        Override method to get queryset depending on the url kwargs
        """

        # Get the model
        model = UserTypeModelFactory().get_suitable_model(
            self.request.user.type.lower()
        )
        queryset = model.objects.all()
        return queryset
