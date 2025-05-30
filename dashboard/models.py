# from django.db import models

# class User(models.Model):
#     phone = models.CharField(max_length=11, unique=True)

#     def __str__(self):
#         return self.phone

# class OtpCode(models.Model):
#     phone = models.CharField(max_length=11)
#     code = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.phone}: {self.code}"
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.sessions.models import Session
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, phone, fullname, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone field must be set')
        user = self.model(phone=phone, fullname=fullname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, fullname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone, fullname, password, **extra_fields)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Role(models.Model):
    name = models.CharField(max_length=32)
    display_name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities', null=True, blank=True)

    def __str__(self):
        return self.name


class MediaUser(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='media/', null=True, blank=True)
    subject_type = models.IntegerField(choices=[
        (1, 'avatar'),
        (2, 'thumbnail'),
        (3, 'gallery'),
        (4, 'event'),
        (5, 'small_thumbnail'),
    ], default=1, blank=True, null=True)

    def __str__(self):
        return f"{self.user.fullname} - {self.id}"



class User(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOICES = (
        (-1, 'rejected'),
        (0, 'pending'),
        (1, 'active'),
    )

    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=11, unique=True)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, related_name='users', blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, related_name='users', blank=True, null=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    avatar = models.ForeignKey(MediaUser, on_delete=models.DO_NOTHING, related_name='avatars', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['fullname']

    # Define groups and user_permissions fields with related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Custom related name to avoid conflicts
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Custom related name to avoid conflicts
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.fullname

class OtpCode(models.Model):
    phone = models.CharField(max_length=11)
    ip_address = models.CharField(max_length=255)
    code = models.PositiveIntegerField()
    token = models.CharField(max_length=255, null=True, blank=True)
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone


class Company(models.Model):
    STATUS_CHOICES = (
        (-1, 'rejected'),
        (0, 'pending'),
        (1, 'active'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies')
    name = models.CharField(max_length=255)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def active_company(sender, instance, created, **kwargs):
    if instance.role and instance.role.id == 4 and instance.status == 1:
        Company.objects.filter(owner=instance).update(status=1)


@receiver(post_save, sender=Company)
def active_user(sender, instance, created, **kwargs):
    if instance.status == 1:
        instance.owner.status = 1
        instance.owner.save()
