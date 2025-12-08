from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Student, StudentProfile

@receiver(post_save, sender=Student)
def create_student_user(sender, instance, created, **kwargs):
    """
    Signal to automatically create a User when a Student is created
    """
    # Check if this is a raw save (like from fixtures) - skip if true
    if kwargs.get('raw', False):
        return
    
    # Only create user for new students
    if created:
        # Generate username from admission_number
        username = f'stu_{instance.admission_number}'
        password = f'{instance.admission_number}'
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            print(f"User {username} already exists. Skipping creation.")
            return
        
        # Create the User
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=instance.email,
                first_name=instance.first_name or '',  # Handle None values
                last_name=instance.last_name or ''     # Handle None values
            )

            # Create student profile linking User and Student
            StudentProfile.objects.create(
                student=instance,
                user=user
            )
            
            print(f"User created successfully: {username}")
            print(f"StudentProfile created for {instance.admission_number}")
            
        except Exception as e:
            print(f'Error creating user for {instance.admission_number}: {e}')


@receiver(post_save, sender=User)
def save_student_profile(sender, instance, **kwargs):
    '''Save student profile when the user is saved'''
    if hasattr(instance, 'student_profile'):
        instance.student_profile.save()