from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

   # path('login/', auth_views.LoginView.as_view(), name='login'),
   # path('logout/', auth_views.LogoutView.as_view(), name='login'),

   # Incluye el formulario para cambiar la contraseña
   # path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
   # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),  name='password_change_done'),

   # reset password urls
   #  path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
   #  path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
   #  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   #  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('', views.dashboard, name='dashboard'),

    # Pag. 137
    path('account/', include('django.contrib.auth.urls')),  # De esta manera se usan las urls propias de Django
    path('register/', views.register, name='register'),  # Registrar un nuevo usuario y Profile asociándole el User recién creado
    path('edit/', views.edit, name='edit'),  # Dos form en 1 para editar User y Profile

    # Pag. 203
    path('users/follow/', views.user_follow, name='user_follow'),

    # Pag. 198
    path('users/', views.user_list, name='user_list'),
    path('users/<username>/', views.user_detail, name='user_detail')
]
