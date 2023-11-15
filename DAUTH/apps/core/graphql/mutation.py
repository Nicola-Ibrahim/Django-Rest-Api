"""graphql mutation file

This file works as an autoloader for all of our defined mutations for all of our models
it iterates over all inner directories and grabs the mutation classes and appends it to
graphql schema file
"""
import os
from inspect import getmembers, isclass

import graphene

from ..utils.generic_helpers import get_file_sub_dirs, import_module_by_path


class MutationAbstract(graphene.ObjectType):
    """Abstract class for base Mutation type"""


# This list will store all the mutation classes defined in different modules
mutations_base_classes = []

# This function will return the current directory and its subdirectories as a tuple
current_directory, subdirectories = get_file_sub_dirs(__file__)

# Print the current directory and subdirectories for debugging purposes
print(current_directory, subdirectories)


for directory in subdirectories:
    try:
        # Call the import_module_by_path function with a formatted string as argument
        # This function will import a module by its file path and return it
        # The formatted string contains the current directory, the os separator, the subdirectory name, and the mutations.py file name
        module = import_module_by_path(f"{current_directory}{os.sep}{directory}{os.sep}mutations.py")

        if module:
            # Call the getmembers function with module and isclass as arguments
            # This function will return a list of tuples containing the names and values of all classes defined in the module
            classes = [x for x in getmembers(module, isclass)]

            # Filter the classes list by checking if the name of each class starts with "Mutation"
            # This will return a list of mutation classes defined in the module
            mutations = [x[1] for x in classes if x[0].startswith("Mutation", 0, 8)]

            # Extend the mutations_base_classes list with the mutations list
            mutations_base_classes += mutations

    except ModuleNotFoundError:
        pass

# Reverse the order of the mutations_base_classes list using slicing notation
# This will make sure that the mutation classes are ordered according to their inheritance hierarchy
mutations_base_classes = mutations_base_classes[::-1]
properties = {}

for base_class in mutations_base_classes:
    # Update the properties dictionary with a new key-value pair
    # The key is the name of the base class obtained from its _meta attribute
    # The value is a graphene.Field instance created from the base class using its Field method
    properties.update({base_class._meta.name: base_class.Field()})

# Use the type function to create a new class called Mutations that inherits from MutationAbstract and has properties as its attributes
# This class will represent the root mutation type for all mutation classes defined in different modules
Mutations = type("Mutations", tuple([MutationAbstract]), properties)
