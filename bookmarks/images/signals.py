from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from bookmarks.images.models import Image


# This decorator allow me to connect the receiver function
# to a signal. So:
# - users_like_changed is a receiver function.
# - m2m_changed is a 'model signal'
# So, everytime a object changes, is invoked the
# Image.users_like.through model (table images_image_users_like)
# and execute the function users_like_changed
@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    """
    Alternative option to create a signal.
    -> users_like_changed is a Receiver function.
    So if the m2m_changed is triggered, the function
    Image.users_like.through will be called.
    """
    # Instance will be a Image model
    instance.total_likes = instance.users_like.count()
    instance.save()
