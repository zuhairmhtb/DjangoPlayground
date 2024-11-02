from django.http import HttpResponse, JsonResponse
from django.http.request import HttpRequest
from django.shortcuts import render
from django.middleware.csrf import get_token

def index(request):
    context = {}
    if request.method == 'POST':
        context['message'] = 'Hello, ' + request.POST['name']
    return render(request, 'django_playground/index.html', context=context)


def csrf(request: HttpRequest)->HttpResponse:
    token = get_token(request)
    response = JsonResponse({"csrfToken": token})

    response["X-CSRFToken"] = token
    return response

