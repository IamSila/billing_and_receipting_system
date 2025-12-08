from django.contrib import admin
from .models import Parent,Student, SchoolClass, StudentProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'middle_name', 'last_name', 'phone', 'email', 'created_at', 'updated_at']
    list_filter = ['first_name', 'middle_name', 'last_name', 'created_at']
    search_fields = ['first_name', 'middle_name', 'last_name', 'email', 'phone']

@admin.register(SchoolClass)
class StudentClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'class_name', 'academic_year', 'max_students', 'is_active']
    list_filter = ['id', 'class_name', 'academic_year']
    search_fields = ['id', 'class_name', 'academic_year']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['admission_number','email', 'first_name','middle_name', 'last_name', 'class_id','class_stream', 'date_of_birth', 'term', 'parent_id']
    
class StudentProfileInline(admin.StackedInline):
  model = StudentProfile
  can_delete = False
  verbose_name_plural = 'Student Profile'

class UserAdmin(BaseUserAdmin):
  inlines = [StudentProfileInline]

'''re-register UserAdmin'''
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(StudentProfile)
