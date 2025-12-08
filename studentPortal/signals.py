from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Student, StudentProfile
import random
import string

@receiver(post_save, sender=Student)
def create_student_user(sender, instance, created, **kwargs):
  # Check if this is a raw save (like from fixtures) - skip if true
  if kwargs.get('raw', False):
    return
  """signal to automatically created  a User when a Student is created"""
  if created:
    '''gen the username from the admission_number'''
    username = f'stu_{instance.admission_number}'
    password = f'{instance.admission_number}'

    '''create the User'''
    try:
      user = User.objects.create_user(
        username=username,
        password=password,
        email=instance.email
      )

      '''here we create a student profile linking User and Student'''
      StudentProfile.objects.create(
        student=instance,
        user = user
      )
      print(f"User created successfully")
      print(f"StudentProfile created: ")
    except Exception as e:
      print(f'Error creating user for {instance.admission_number}: {e}')



@receiver(post_save, sender=User)
def save_student_profile(sender, instance, **kwargs):
  '''Sace student profile when the user is saved'''
  if hasattr(instance, 'student_profile'):
    instance.student_profile.save()
