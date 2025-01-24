from django.shortcuts import redirect

def sessionMiddleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        print(request.get_full_path())
        #return response

        if (request.get_full_path() in ['/login', '/register', '/language']):
          if (request.session.get('username') is not None):
            print ('redirecting to /')
            return redirect('/')
          else:
            print ('user not authenticated')
            return response

        if (request.session.get('username') is not None):
          print ('user authenticated')
          return response
        else:
          print ('user not authenticated')
          return redirect('/login')


    return middleware