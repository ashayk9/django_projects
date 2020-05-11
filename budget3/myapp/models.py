from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    dob = models.DateField(null=True, blank=True)
    # intake=models.ForeignKey(ExpenseInfo, on_delete=models.CASCADE)
    # expenditure=models.ForeignKey(ExpenseInfo,on_delete=models.SET_NULL)
    # date_added=models.ForeignKey(ExpenseInfo, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.user.username)


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class ExpenseInfo(models.Model):
    expenditure = models.IntegerField(null=True,blank=True)
    intake = models.FloatField(null=True,blank=True)
    date_added = models.DateTimeField(null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return reverse('create', kwargs={'user':self.user})
