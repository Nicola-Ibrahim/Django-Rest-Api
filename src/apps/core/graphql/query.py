"""graphql query file

This file works as an autoloader for all of our defined queries for all of our models
it iterates over all inner directories and grabs the query classes and appends it to
graphql schema file

INSPIRATION FROM:
    - https://github.com/graphql-python/graphene/issues/545#issuecomment-329630141
"""

import os
from inspect import getmembers, isclass

import graphene
from django.apps import apps
from django.conf import settings
from graphene_django.debug import DjangoDebug

from ..utils.generic_helpers import get_file_sub_dirs, import_module_by_path


class QueriesAbstract(graphene.ObjectType):
    """
    Abstract class for base query
    """

    if settings.DEBUG:
        debug = graphene.Field(DjangoDebug, name="_debug")


queries_base_classes = [QueriesAbstract]
current_directory, subdirectories = get_file_sub_dirs(__file__)

for directory in subdirectories:
    try:
        module = import_module_by_path(f"{current_directory}{os.sep}{directory}{os.sep}queries.py")
        if module:
            classes = [x for x in getmembers(module, isclass)]
            queries = [x[1] for x in classes if "Query" in x[0]]
            queries_base_classes += queries
    except ModuleNotFoundError:
        pass

queries_base_classes = queries_base_classes[::-1]
properties = {}
for base_class in queries_base_classes:
    properties.update(base_class.__dict__["_meta"].fields)

Queries = type("Queries", tuple(queries_base_classes), properties)

# Get a list of app config instances
app_configs = apps.get_app_configs()

# Get a list of custom app names
custom_app_names = [
    app_config.name for app_config in app_configs if app_config.path.startswith(str(settings.BASE_DIR))
]

# Print the list
print(app_configs)
