from django.http import HttpResponseBadRequest

from bookmarks.common.resources import is_ajax


def ajax_required(f):
    def wrap(request, *args, **kwargs):
        # El objeto request de django permite ejecutar el is_ajax()
        # que en otras palabras valida si la request proviene de ajax.
        if not is_ajax(request):
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
