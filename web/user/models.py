from django.db import models
from django.contrib.auth.models import User
from commune.models import Commune
from region.models import Region
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

class UserProfileManager(models.Manager):
    def get_queryset(self):
        return super(UserProfileManager, self).get_queryset()#.filter(city='Santiago')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user', primary_key=True)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    email = models.EmailField(unique=True, blank=False, default='')
    address =  models.CharField(max_length=100, default='')
    phone = models.IntegerField(default=0)
    addressStreet = models.CharField("Calle",max_length=300,default="")
    addressNumber = models.CharField("Numero",max_length=10,default=0)
    addressCommune = models.ForeignKey(Commune,
        on_delete=models.CASCADE,
        verbose_name="Comuna",
        blank=True,
        null=True,
        to_field='code')
    addressRegion = models.ForeignKey(Region,
        on_delete=models.CASCADE,
        verbose_name="Region",
        blank=True,
        null=True,
        to_field='code')



    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        userprofile=UserProfile.objects.create(user=instance, first_name=instance.first_name,
                                                 last_name=instance.first_name, email=instance.email)
        userprofile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.user.save()
    except ObjectDoesNotExist:
        userprofile = UserProfile.objects.create(user=instance, first_name=instance.first_name,
                                                 last_name=instance.first_name, email=instance.email)
        userprofile.save()
        instance.user.save()
