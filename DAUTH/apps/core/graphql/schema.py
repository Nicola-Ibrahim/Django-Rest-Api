"""Full GraphQl schema for SCRIPT project"""
import graphene

from .mutation import Mutations
from .query import Queries


class Query(Queries, graphene.ObjectType):
    """Root query class"""


class Mutation(Mutations, graphene.ObjectType):
    """Root mutation class"""


schema = graphene.Schema(query=Query, mutation=Mutation)
