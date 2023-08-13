import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from ..models import models


class UserFilterSet(django_filters.FilterSet):
    class Meta:
        model = models.User
        filter_fields = {
            "first_name": ["exact", "icontains", "istartswith"],
            "email": ["exact"],
            "is_verified": ["exact"],
        }


class UserType(DjangoObjectType):
    class Meta:
        model = models.User
        filterset_class = UserFilterSet
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    user = graphene.relay.Node.Field(UserType)
    users = DjangoFilterConnectionField(UserType)
