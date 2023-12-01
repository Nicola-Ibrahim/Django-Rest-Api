from rest_framework import renderers


class ErrorRenderer(renderers.JSONRenderer):
    """Custom error renderer"""

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ""
        if "ErrorDetail" in str(data):
            response = super().render({"error": data["error"]}, accepted_media_type, renderer_context)
        return response


class DataRenderer(renderers.JSONRenderer):
    """Custom data renderer"""

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ""
        if "ErrorDetail" not in str(data):
            response = super().render({"data": data}, accepted_media_type, renderer_context)
        return response
