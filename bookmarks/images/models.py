from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, 
                               db_index=True)  # Es una buena práctica sobre atributos
                                               # que son consultados atraves de filter(), 
                                               # order_by(), y/o exclude()
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,  # Un usuário pode curtir varias imágenes,
                                                                   # y las imagenes pueden ser curtidas por
                                                                   # varios usuarios.
                                        related_name='images_liked',  # permite acceder a los objetos 
                                                                      # relacionados con image.users_like.all()
                                                                      #  o users.images_liked.all() 
                                        blank=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Ex.: https://127.0.0.1:8000/images/detail/6/alexa/
        return reverse('images:detail', args=[self.id, self.slug])
    
    
    def save(self, *args, **kwargs):
        """Al crear una imagen le va a poner el slug al objeto automáticamente."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
