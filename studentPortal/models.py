import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import AutoField

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
    email = models.EmailField(
        blank=True,
        null=True,
        help_text="Optional - Used for sending PDF version of invoices",
    )

    # System field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "parents"
        verbose_name = "Parent"
        verbose_name_plural = "Parents"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# school classes table
class SchoolClass(models.Model):
    STREAM_CHOICES = [
        ("A", "streamA"),
        ("B", "streamB"),
        ("C", "streamC"),
        ("D", "streamD"),
    ]
    id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=50)
    stream = models.CharField(
        max_length=10, blank=True, null=True, choices=STREAM_CHOICES
    )
    academic_year = models.CharField(max_length=20)
    max_students = models.IntegerField()
    is_active = models.BooleanField(default=True)


# student table


class Student(models.Model):
    """
    Student model
    """

    # Admission Information
    admission_number = models.CharField(primary_key=True, max_length=50, unique=True)
    email = models.EmailField()

    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True) or ""
    date_of_birth = models.DateField()

    # Academic Information
    class_id = models.ForeignKey(
        "SchoolClass", on_delete=models.PROTECT, related_name="student_class"
    )

    # These choices must be similar to those in the classes.
    STREAM_CHOICES = [
        ("A", "streamA"),
        ("B", "streamB"),
        ("C", "streamC"),
        ("D", "streamD"),
    ]
    class_stream = models.CharField(
        max_length=20, blank=True, null=True, choices=STREAM_CHOICES
    )

    # Parent/Guardian Information
    parent_id = models.ForeignKey(
        "Parent", on_delete=models.PROTECT, related_name="parent"
    )

    # Academic Term
    TERM_CHOICES = [
        ("TERM1", "Term1"),
        ("TERM2", "Term2"),
        ("TERM3", "Term3"),
    ]
    term = models.CharField(max_length=10, choices=TERM_CHOICES)

    # Billing Information
    billing_profile_active = models.BooleanField(default=True)

    """we use this function to fetch a student's fee structure"""

    def get_fee_structure(self):
        return FeeStructure.objects.filter(school_class=self.class_id).first()

    class Meta:
        db_table = "students"
        ordering = ["admission_number"]

    def __str__(self):
        return f"{self.admission_number} - {self.first_name} {self.last_name}"


class StudentProfile(models.Model):
    student = models.OneToOneField(
        Student, on_delete=models.CASCADE, related_name="profile"
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="student_profile"
    )

    def __str__(self):
        return f"Profile for {self.student.admission_number}"


"""this model stores the school fees"""


class FeeStructure(models.Model):
    """
    Fee structure for a specific class + academic year
    """

    school_class = models.ForeignKey(
        SchoolClass, on_delete=models.PROTECT, related_name="fee_structures"
    )

    academic_year = models.CharField(max_length=20)

    # Example fee components
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)
    lunch_fee = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    transport_fee = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    other_fees = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    # Track updates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "fee_structures"
        unique_together = ("school_class", "academic_year")
        verbose_name = "Fee Structure"
        verbose_name_plural = "Fee Structures"

    def __str__(self):
        return f"{self.school_class.class_name} - {self.academic_year}"
