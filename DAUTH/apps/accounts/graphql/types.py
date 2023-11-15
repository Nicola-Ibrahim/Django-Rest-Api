from graphene_django import DjangoObjectType

from ..models import models


class UserType(DjangoObjectType):
    class Meta:
        model = models.User
        fields = "__all__"
