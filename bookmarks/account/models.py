from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings


class Profile(models.Model):
    # Pag. 141
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'

class Contact(models.Model):
    """
    Pag 192.
    Creando un modelo intermediario para relacionar usuarios.
    Es útil cuando se usa el User de Django y no se quiere tocar
    y/o cuando se requiere guardar cuando fue creada esta relación.
    Además al tener la relación en una tabla a parte, se evita hacer
    joins.
    """
    # Usuario que cria la relación
    user_from = models.ForeignKey('auth.User',
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    # Usuario que está siendo seguido
    user_to = models.ForeignKey('auth.User',
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    # Guarda el instante en que fue creada la relación
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    # Así se crearía una relación
    # user1 = User.objects.get(id=1)
    # user2 = User.objects.get(id=1)
    # Contact.objects.create(user_from=user1, user_to=user2)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'

# Pag 194.
# A continuación se agrega el attr 'following' al modelo User
# propio de django, usando la relación muchos a muchos
# con los campos descritos en la clase ManyToManyField
# Si el modelo User fuese propio y no de Django, entonces
# se agregaría esto directo en la clase.
user_model = get_user_model()  # Retorna el modelo de usuario usado en el proyecto
# add_to_class permite hacer un monkey patch en el modelo User
user_model.add_to_class('following',
                        models.ManyToManyField('self',
                                                through=Contact,
                                                related_name='followers',  # Esto permite hacer queries así:
                                                                    # user.followers.all() o user.following.all()
                                                symmetrical=False))  # Pag 195. Esto significa en el contexto de la app
                                                                    # que si yo te sigo no significa que tu me sigas