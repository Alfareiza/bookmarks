import redis
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from .forms import ImageCreateForm
from .models import Image
from ..common.decorators import ajax_required
from ..common.resources import is_ajax
from ..actions.utils import create_action
from ..settings import REDIS_HOST, REDIS_PORT, REDIS_DB

# Chapter 6
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


# @login_required
def image_create(request):
    if request.method == 'POST':
        # Usuario clicó en submit
        form = ImageCreateForm(data=request.POST)
        # reuest.POST ->  {'title': [' Este es un ejemplo'], 'url': ['https://cdn.vectorstock.com/i/preview-1x/45/17/cool-hand-drawn-of-python-with-red-and-green-vector-45904517.jpg']}
        if form.is_valid():  # Ejecuta el clean_url()
            cd = form.cleaned_data  # Al haber ejecutado el clean_url, me da acceso a este attr
            new_item = form.save(commit=False)  # Ejecuta save sobrescrito en forms.py
            # atribuye el usuario actual al item
            new_item.user = request.user  # new_item es un obj del modelo Image
            new_item.save()  # Guarda objeto en bd, este save() es del modelo.

            create_action(request.user, 'bookmarked image', new_item)

            messages.success(request, 'Image added successfully')

            # redirecciona para la view de detalles del nuevo item creado
            return redirect(new_item.get_absolute_url())
    else:
        # Crea el formulario con la informacion básica del form
        form = ImageCreateForm(
            data=request.GET  # De esta manera se le puede enviar data al form desde la url
            # https://localhost:8000/images/create/?title=%20Este%20es%20un%20ejemplo&url=https://cdn.vectorstock.com/i/preview-1x/45/17/cool-hand-drawn-of-python-with-red-and-green-vector-45904517.jpg
        )

    return render(request, 'images/image/create.html', {'section': 'images', 'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # Crea la llave 'image:33:id' e incrementa
    # en 1 las visualizaciones y lo devuenve a la variable
    total_views = r.incr(f'image:{image.id}:views')
    # Crea la llave image:ranking y guarda las visualizaciones
    # en un conjunto ordenado
    # Incremente en 1 el ranking de la imagen
    r.zincrby('image_ranking', 1, image.id)
    return render(request,
                  'images/image/detail.html',
                  {'section': 'images',  # Ver en base.html que cuando se envia este parametro, activa algo en el html
                   'image': image,
                   'total_views': total_views})


@ajax_required  # Decorator para limitar requests que vengan solo de XMLHttpRequest
@login_required
@require_POST  # Si no es llamado con POST retorna un Obj HttpResponseNotAllowed con 405 Pag. 182
def image_like(request):
    """
    Recibirá solamente requests generados por medio de ajax.
    Por eso hay que validar el campo HTTP_X_REQUESTED_WITH
    request.META.HTTP_X_REQUESTED_WITH -> 'XMLHttpRequest'
    """
    image_id = request.POST.get('id')
    action = request.POST.get('action')  # Puede ser like o unlike
    if image_id and action:
        try:
            # Pag 182.
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)  # Al objeto image, le agrega aquel usuario
                # Tmbn existe la opción clear() que limpia la relación.
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)  # Al objeto image, le quita aquel usuario
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})


@login_required
def image_list(request):
    """
    Pag. 188.
    Por defecto se renderizará el list.html que contendrá
    las primeras 8 imágenes y extenderá el list_ajax.html
    que será renderizado a traves de ajax.
    En caso sea llamada esta vista desde ajax, entonces
    renderizará list_ajax.html
    """
    images = Image.objects.all()
    paginator = Paginator(images, 8)  # Obtiene 8 imagens por pagina
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        # Si la pagina requisitada esta fuera del intervalo
        if is_ajax(request):
            # If the request is AJAX and the page is out of range
            # return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    if is_ajax(request):
        return render(request,
                      'images/image/list_ajax.html',
                      {'section': 'images', 'images': images})
    return render(request,
                  'images/image/list.html',
                  {'section': 'images', 'images': images})


@login_required
def image_ranking(request):
    # get image ranking dictionary
    # This commands waits a customize interval
    # with the lowest and the highest punctuation
    # So 0 is the lowest and -1 is the highest (like infinite)
    # desc=True will reach the result decreasingly
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]  # [b'12', b'10', b'6']
    # Basically transform all the elements in integers
    image_ranking_ids = [int(id) for id in image_ranking]
    # get most viewed images
    # Make the list cast only because later will be necessary to use the sort function
    most_viewed = list(Image.objects.filter(
                           id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(request,
                  'images/image/ranking.html',
                  {'section': 'images',
                   'most_viewed': most_viewed})