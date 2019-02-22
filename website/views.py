from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, stranger. Have you ever heard about birana?")

def ping(request):
    return HttpResponse('pong')
