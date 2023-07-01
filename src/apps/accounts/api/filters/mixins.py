from .factories import UserTypeFilterBackend


class FilterMixin:
    filter_backends = [
        UserTypeFilterBackend,
    ]
