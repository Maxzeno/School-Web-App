from django.db import models
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)

# Create your models here.

class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **extra_fields)
        user.save(using=self._db)
        return user

    def create(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)


    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, unique=True)
    _password = ''
    is_staff = models.BooleanField(default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(default=True)

    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_semiadmin = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def save(self, *args, **kwargs):
        u = self.__class__.objects.filter(pk=self.pk).first()
        if not u or u and u.password != self.password:
            self.set_password(self.password)
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        swappable = 'AUTH_USER_MODEL'


"""
['Aggregate', 'AutoField', 'Avg', 'BLANK_CHOICE_DASH', 'BigAutoField', 'BigIntegerField', 'BinaryField', 'BooleanField', 'CASCADE', 
'Case', 'CharField', 'CheckConstraint', 'Choices', 'CommaSeparatedIntegerField', 'Count', 'DEFERRED', 'DO_NOTHING', 'DateField', 
'DateTimeField', 'DecimalField', 'Deferrable', 'DurationField', 'EmailField', 'Empty', 'Exists', 'Expression', 'ExpressionList', 
'ExpressionWrapper', 'F', 'Field', 'FileField', 'FilePathField', 'FilteredRelation', 'FloatField', 'ForeignKey', 'ForeignObject', 
'ForeignObjectRel', 'Func', 'GenericIPAddressField', 'IPAddressField', 'ImageField', 'Index', 'IntegerChoices', 'IntegerField', 
'JSONField', 'Lookup', 'Manager', 'ManyToManyField', 'ManyToManyRel', 'ManyToOneRel', 'Max', 'Min', 'Model', 'NOT_PROVIDED', 
'NullBooleanField', 'ObjectDoesNotExist', 'OneToOneField', 'OneToOneRel', 'OrderBy', 'OrderWrt', 'OuterRef', 'PROTECT', 
'PositiveBigIntegerField', 'PositiveIntegerField', 'PositiveSmallIntegerField', 'Prefetch', 'ProtectedError', 'Q', 'QuerySet', 
'RESTRICT', 'RestrictedError', 'RowRange', 'SET', 'SET_DEFAULT', 'SET_NULL', 'SlugField', 'SmallAutoField', 'SmallIntegerField', 
'StdDev', 'Subquery', 'Sum', 'TextChoices', 'TextField', 'TimeField', 'Transform', 'URLField', 'UUIDField', 'UniqueConstraint', 
'Value', 'ValueRange', 'Variance', 'When', 'Window', 'WindowFrame', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', 
'__loader__', '__name__', '__package__', '__path__', '__spec__', 'aggregates', 'aggregates_all', 'base', 'constants', 'constraints', 
'constraints_all', 'deletion', 'enums', 'enums_all', 'expressions', 'fields', 'fields_all', 'functions', 'indexes', 'indexes_all', 
'lookups', 'manager', 'options', 'prefetch_related_objects', 'query', 'query_utils', 'signals', 'sql', 'utils']
"""

