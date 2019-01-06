from django.db import models
from django.contrib.auth.models import User
from appraisal.models import Appraisal
from commune.models import Commune
from region.models import Region
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.core.mail import send_mail
from django.template import loader

class Notification(models.Model):
    ntype = models.CharField(max_length=100, default='')
    appraisal_id = models.IntegerField(null=True)
    comment_id = models.IntegerField(null=True)
    time_created = models.DateTimeField("Time created",blank=True,null=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user', primary_key=True)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    email = models.EmailField(unique=True, blank=False, default='')
    address =  models.CharField(max_length=100, default='')
    phone = models.IntegerField(default=0)
    rut = models.CharField('RUT', max_length=14, null=True)
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
    notifications = models.ManyToManyField(Notification)

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
    def full_name(self):
        return self.first_name + " " + self.last_name

    @property
    def rut_verbose(self):
        return "16.017.511-7"

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
    
    def removeNotification(self,ntype="",appraisal_id="",comment_id=""):
        if ntype == "comment":
            notifications = self.notifications.all().filter(appraisal_id=appraisal_id)
            for notification in notifications:
                self.notifications.remove(notification)

    def addNotification(self,ntype="",appraisal_id="",comment_id=""):
        n = Notification(
            ntype=ntype,
            appraisal_id=appraisal_id,
            comment_id=comment_id,
            time_created=datetime.datetime.now(datetime.timezone.utc))
        appraisal = Appraisal.objects.get(id=appraisal_id)
        html_message = loader.render_to_string('user/email_solicitud.html',{'user':self.user,'appraisal': appraisal})
        send_mail(
            subject='Asignación de tasación',
            message='',
            from_email='soporte@dataurbana.io',
            recipient_list=['nicorivas@gmail.com'],
            fail_silently=False,
            html_message=html_message
        )
        '''
        'Estimado '+self.full_name+',\n\n'+"""
                ProTasa le ha solicitado una nueva tasación.
                Dirección: """+appraisal.real_estates.first().address+""".
                Tipo de propiedad: """+appraisal.real_estates.first().address+""".
                Para obtener más información, haga <a href="a">click aquí</a>"""
        '''
        n.save()
        self.notifications.add(n)

    def hasNotificationAppraisal(self,id):
        '''
        Check if there is a notification for this user
        related to the appraisal given by the id
        '''
        for notification in self.notifications.all():
            if notification.ntype == "comment":
                if notification.appraisal_id == id:
                    return True
        return False

    def hasNotificationComment(self,id):
        '''
        Check if there is a notification for this user
        related to the comment given by the id
        '''
        for notification in self.notifications.all():
            if notification.ntype == "comment":
                if notification.comment_id == id:
                    return True
        return False

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
