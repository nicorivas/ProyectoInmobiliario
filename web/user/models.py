from django.db import models
from django.contrib.auth.models import User
from commune.models import Commune
from region.models import Region
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


class UserProfile(models.Model):
    rut = models.CharField('RUT', max_length=14)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user', primary_key=True)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    email = models.EmailField(unique=True, blank=False, default='')
    address =  models.CharField(max_length=100, default='')
    phone = models.IntegerField(default=0)
    addressStreet = models.CharField("Calle",max_length=300,default="")
    addressNumber = models.CharField("Numero",max_length=10)
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

    @property
    def has_address(self):
        if self.addressStreet == None or self.addressCommune == None or self.addressRegion == None:
            return False
        else:
            return True

    @property
    def address(self):
        if not self.has_address:
            return ''
        else:
            return self.addressStreet+' '+str(self.addressNumber)+', '+self.addressCommune.name+', '+self.addressRegion.shortName

    @property
    def badge(self):
        if self.user.is_superuser:
            return '<div class="badge badge-dark">Superuser</div>'
        groups = self.user.groups.values_list('name',flat=True)
        if 'tasador' in groups:
            return '<div class="badge badge-success">Tasador</div>'
        elif 'visador' in groups:
            return '<div class="badge badge-success">Visador</div>'
        elif 'asignador' in groups:
            return '<div class="badge badge-success">Asignador</div>'
        else:
            return ''
    

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance, first_name=instance.first_name,
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
