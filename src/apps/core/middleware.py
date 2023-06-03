from django.utils.translation import activate


class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the lang parameter from the URL
        lang = request.GET.get("lang", "en")

        # Activate the language for the current thread
        activate(lang)

        # Call the next middleware or view
        response = self.get_response(request)

        return response
