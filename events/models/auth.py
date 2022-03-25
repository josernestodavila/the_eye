from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
)


class ApplicationManager(BaseUserManager):
    def create_user(self, name: str, password=None):
        """
        Creates and saves an Application with the given name and password.
        """
        if not name:
            raise ValueError("Application must have a name")

        application = self.model(name=name)
        application.set_password(password)
        application.save(using=self._db)

        return application

    def create_superuser(self, name: str, password=None):
        """
        Creates and saves a superuser Application with the given
        name and password.
        """
        application = self.create_user(name, password)
        application.is_admin = True
        application.save(using=self._db)

        return application


class Application(AbstractBaseUser):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = ApplicationManager()

    USERNAME_FIELD = "name"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
