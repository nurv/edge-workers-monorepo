from django.apps import AppConfig


class BucketsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'buckets'

    def ready(self) -> None:
        from buckets import signals