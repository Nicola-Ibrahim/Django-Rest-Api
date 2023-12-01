"""
This file script should be imported in the ready()
method in apps.py file
For ensuring to be recognizable by the server
"""

from django.dispatch import Signal

user_proxy_model_instance_saved = Signal()
