from django.shortcuts import render


def e_handler404(request, exception):
    context = {}
    response = render(request, "misc/404.html", context=context)
    response.status_code = 404
    return response


def e_handler500(request):
    context = {}
    response = render(request, "misc/404.html", context=context)
    response.status_code = 500
    return response
