from django.apps import AppConfig




class ImagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookmarks.images'

    def ready(self):
        # Import the handlers of signals
        from bookmarks.images import signals
