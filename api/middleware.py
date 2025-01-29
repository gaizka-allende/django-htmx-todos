from django.shortcuts import redirect

def sessionMiddleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):

        response = get_response(request)

        if (request.get_full_path() in ['/login', '/register']) and (request.method == 'POST'):
          return response

        if (request.get_full_path() in ['/login', '/logout', '/register', '/language']):
          if (request.session.get('username') is not None):
            return redirect('/')
          else:
            return response

        if (request.session.get('username') is not None):
          return response
        else:
          return redirect('/login')


    return middleware