from django.apps import AppConfig


class HumanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'human'

# class UsersConfig(AppConfig):
#     name = 'users'

    def ready(self):
        import human.signals