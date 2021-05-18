from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class MyUser(models.Model):
    USER_TYPE = (
        ('AD', 'admin'),
        ('IN', 'instructor'),
        ('TA', 'ta'),
    )
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    # user_pk = models.IntegerField(blank=True)

    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, unique = True)
    user_type = models.CharField(max_length=2, choices=USER_TYPE)
    ta_count = models.IntegerField(0)

class Course(models.Model):
    name = models.CharField(max_length=20)
    subject = models.CharField(max_length=50)
    course_number = models.CharField(max_length=50)
    section_instructor = models.CharField(max_length=50)
    lab_ta = models.CharField(max_length=50)
    section_number = models.CharField(max_length=50)




# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         MyUser.objects.create(user=instance, user_pk=instance.id)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.myuser.save()