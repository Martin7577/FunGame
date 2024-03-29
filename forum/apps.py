from django.apps import AppConfig


class ForumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forum'

# class AccountsConfig(AppConfig):
#     name = 'forum'
#
#     def ready(self):
#         import forum.signals
