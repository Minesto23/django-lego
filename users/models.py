from django.db import models
# We import the class for create our custom user
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Define my user manger 
class CustomUserManager(BaseUserManager):
    
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('Users must have an username')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a superuser with the given username, email,
        and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# We define my custom user models

class CustomUser(AbstractBaseUser):
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        verbose_name='username',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='first name',
        max_length=50,
    )
    last_name = models.CharField(
        verbose_name='last name',
        max_length=50,
    )
    # we can create more fields in for our user

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_all_permissions(self, obj=None):
        return [] 

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
