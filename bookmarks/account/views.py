from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from bookmarks.account.forms import ProfileEditForm, UserEditForm, UserRegistrationForm
from bookmarks.account.models import Contact, Profile
from bookmarks.actions.models import Action
from bookmarks.actions.utils import create_action
from bookmarks.common.decorators import ajax_required


@login_required
def dashboard(request):
    # All the actions except the actions of the current user
    actions = Action.objects.exclude(user=request.user)

    # List all ids of the following users. Ex.: [1, 2, 5, 9]
    if following_ids := request.user.following.values_list('id', flat=True):
        # Get the actions which are in the ids of the following users
        actions = actions.filter(user_id__in=following_ids)
    # In select_related It's used user__profile to make join between user and profile tables
    # In prefetch_related It's used to execute separate selects
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard', 'actions': actions})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)  # Crea objeto User, sin guardar en bd
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()

            # Por cada User nuevo, se creará un Profile
            Profile.objects.create(user=new_user)

            create_action(new_user, 'has created an account')
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,
                  'account/user/list.html',
                  {'section': 'people',
                   'users': users})

@login_required
def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    return render(request,
                  'account/user/detail.html',
                  {'section': 'people',
                   'user': user})

# Pag. 201
# Función parecida con image_like que se ejecuta cuando es clicado el boton de seguir
# en la vista de detail.html el cual viene desde ajax.
# Dicha petición a la vista se puede bloquear si no fuese tipo ajax.
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})