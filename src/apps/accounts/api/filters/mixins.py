from .factories import UserTypeFilterFactory


class FilterMixin:
    filter_backends = [
        UserTypeFilterFactory,
    ]
