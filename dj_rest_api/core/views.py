from django.shortcuts import render


def handler404(request, exception, template_name="404.html"):
    response = render(request, "core/404_not_found.html", status=404)
    return response
