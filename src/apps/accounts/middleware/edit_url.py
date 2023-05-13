# from django.contrib.sites.shortcuts import get_current_site
# from rest_framework.reverse import reverse

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


class EditUrlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # Change the url after processing the view

        if request.method == "GET":
            request.path += "1/"

        if request.method == "POST":
            request.path += "1/"

        if request.method == "DELETE":
            request.path += "1/"

        print(request.user)
        print(request.path)
        print(request.path_info)
        print("-" * 40)
        # Code to be executed for each request/response after
        # the view is called.
        response = self.get_response(request)

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Called just before Django calls the view.
        """

        return None

    def process_exception(self, request, exception):
        """
        Called when a view raises an exception.
        """
        return None

    def process_template_response(self, request, response):
        """
        Called just after the view has finished executing.
        """
        return response
