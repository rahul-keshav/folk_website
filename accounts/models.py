from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class UserAccountManager(models.Manager):
    def get_queryset(self):
        return super(UserAccountManager, self).get_queryset().filter(city='jaipur')

class UserAccount(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    discription=models.CharField(max_length=50)
    contact_no=models.CharField(max_length=15)
    city=models.CharField(max_length=20)
    website=models.CharField(max_length=20)
    image=models.ImageField(upload_to='profile_image',blank=True)

    objects = UserAccountManager()

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserAccount.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)