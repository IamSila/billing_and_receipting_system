from django.apps import AppConfig


class StudentportalConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "studentPortal"


class StudentConfig(AppConfig):
  default_auto_field = 'django.db.models.BigAutoField'
  name = 'studentPortal'
  def ready(self):
    import studentPortal.signals
    print("student signals loaded")
