from django.db import models
from django.db.models.query import AutoField
import uuid

# create your models here
class Parent(models.Model):
    """
    Parent/Guardian model
    """
    # Primary Key (auto-generated UUID)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    
    # Contact Information
    phone = models.CharField(max_length=20, help_text="Used for sending SMS")
    email = models.EmailField(blank=True, null=True, help_text="Optional - Used for sending PDF version of invoices")
    
    # System field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'parents'
        verbose_name = 'Parent'
        verbose_name_plural = 'Parents'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"



# school classes table
class SchoolClass(models.Model):
    STREAM_CHOICES = [
        ('A', 'streamA'),
        ('B', 'streamB'),
        ('C', 'streamC'),
        ('D', 'streamD'),
    ]
    id = models.AutoField(primary_key=True)
    class_name =models.CharField(max_length=50)
    stream = models.CharField(max_length=10,blank=True, null=True, choices=STREAM_CHOICES)
    academic_year = models.CharField(max_length=20)
    max_students = models.IntegerField()
    is_active = models.BooleanField(default=True)


# student table

class Student(models.Model):
    """
    Student model
    """
    # Primary Key (auto-generated)
    id = models.AutoField(primary_key=True)
    
    # Admission Information
    admission_number = models.CharField(max_length=50, unique=True)
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField()
    
    # Academic Information
    class_id = models.ForeignKey('SchoolClass', on_delete=models.PROTECT)

    #These choices must be similar to those in the classes.
    STREAM_CHOICES = [
        ('A', 'streamA'),
        ('B', 'streamB'),
        ('C', 'streamC'),
        ('D', 'streamD'),
    ]
    class_stream = models.CharField(max_length=20, blank=True, null=True, choices=STREAM_CHOICES)
    
    # Parent/Guardian Information
    parent_id = models.ForeignKey('Parent', on_delete=models.PROTECT)
    
    # Academic Term
    TERM_CHOICES = [
        ('TERM1', 'Term1'),
        ('TERM2', 'Term2'),
        ('TERM3', 'Term3'),
    ]
    term = models.CharField(max_length=10, choices=TERM_CHOICES)
    
    # Billing Information
    billing_profile_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'students'
        ordering = ['admission_number']
    
    def __str__(self):
        return f"{self.admission_number} - {self.first_name} {self.last_name}"
