from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify
import certifi


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {'url': forms.HiddenInput}
  
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ('jpg', 'jpeg')
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not '
                                        'match valid image extensions.')
        return url
    
    def save(self, force_insert=False, force_update=False, commit=True):
        """
        Siempre que se guarde el formulario se ejecutará esta 
        función.
        Guarda la instancia actual del modelo en la bd y retorna
        un objeto.
        :param force_insert:
        :param force_update:
        :param commit: Si es True, guardará el obj en la bd, sino no.
        """
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']  # Creo que aqui ejecuta el clean_url
        name = slugify(image.title)
        extension = image_url.rsplit('-', 1)[1].lower()
        image_name = f'{name}.{extension}'


        # Descarga la imagen a partir de la URL especificada
        response = request.urlopen(image_url,cafile=certifi.where())
        image.image.save(image_name,
                         ContentFile(response.read()),
                         save=False)

        if commit:
            image.save()

        return image
