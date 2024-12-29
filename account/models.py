from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.



class UserManager(BaseUserManager):

	def create_user(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError('email field must be set!')
		user = self.model(
			email=email,
			**extra_fields
			)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superadmin', True)
		extra_fields.setdefault('is_admin', True)
		extra_fields.setdefault('is_active', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superadmin') is not True:
			raise ValueError('Superuser must have is_superadmin=True.')
		
		return self.create_user(email=email, password=password, **extra_fields)


class AuthUser(AbstractBaseUser):

	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField(unique=True)
	mail_verified = models.BooleanField(default=False)

	joined_date = models.DateTimeField(auto_now_add=True)
	last_login = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	is_agreed = models.BooleanField(default=True)
	is_superadmin = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name']

	objects = UserManager()

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, add_label):
		return True

	def is_verified(self):
		return self.mail_verified

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)


class UserProfile(models.Model):
	GENDER_CHOICE = [
		('MALE','MALE'),
		('FEMALE','FEMALE'),
		('OTHERS','OTHERS'),
	]

	user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name='profile')
	image = models.ImageField(upload_to='media/user_profile/', null=True, blank=True)
	age = models.IntegerField(null=True, blank=True)
	gender = models.CharField(choices=GENDER_CHOICE, max_length=50, null=True, blank=True)


	def __str__(self):
		return f'{self.user.email}'

@receiver(post_save, sender=AuthUser)
def create_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)



class BlacklistedToken(models.Model):
    token = models.CharField(max_length=512, unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token