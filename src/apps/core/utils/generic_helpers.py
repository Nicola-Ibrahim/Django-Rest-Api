"""
Utils module for generic helpers
"""
import importlib
import os
import sys


def import_module_by_path(path: str):
    """
    Helper function for importing module by path
    :param path: the path of module to be loaded
    :return: loaded module
    """
    try:
        spec = importlib.util.spec_from_file_location("module.name", path)
        m = importlib.util.module_from_spec(spec)

        sys.modules["module.name"] = m
        spec.loader.exec_module(m)
        return m
    except FileNotFoundError:
        pass


def get_file_sub_dirs(file: str):
    """
    Helper function for discovering the sub dirs of file
    :param file:
    :return: tuple of directory and subdirectories of file
    """
    file_directory = os.path.dirname(os.path.abspath(file))
    file_subdirectories = [
        sub_dir
        for sub_dir in os.listdir(file_directory)
        if os.path.isdir(os.path.join(file_directory, sub_dir)) and sub_dir != "__pycache__"
    ]
    return file_directory, file_subdirectories
