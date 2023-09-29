from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Pag 205.
class Action(models.Model):
    """
    Creado para guardar las actividades del usuario con el objetivo
    de lograr un timeline.
    """
    # Usuario que ejecutó la acción
    user = models.ForeignKey('auth.User',
                             related_name='actions',
                             db_index=True,
                             on_delete=models.CASCADE)

    # Verbo que define la acción del usuario, Ej.: 'le dió like a una imagen'
    verb = models.CharField(max_length=255)

    # Momento en que fue ejecutada la acción
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    # Pag 207.
    # Agregando relacionamentos genericos al modelo Actions
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj',
                                  on_delete=models.CASCADE)

    # Guarda la llave primaria del objeto relacionado
    target_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)

    # Relaciona los dos campos anteriores
    # Esto no crea campo en la base de datos
    target = GenericForeignKey('target_ct', 'target_id')

    class Meta:
        ordering = ('-created',)