from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from my_awesome_project.payments.utils import Paddle


@csrf_exempt
def paddle_webhook(request):
    if request.method == "POST":
        paddle = Paddle(request.POST)
        if paddle.is_valid:
            paddle.process_webhook()
            return HttpResponse("")
    return HttpResponseBadRequest()
