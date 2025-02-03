from django.shortcuts import redirect

def sessionMiddleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        response = get_response(request)
        return response


    return middleware