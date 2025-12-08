from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class StudentRegistrationForm(forms.ModelForm):
    """
    Form for registering new students (admin/staff use)
    """
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Student
        fields = ['admission_number', 'first_name', 'last_name', 'email', 'date_of_birth']
        
    def clean_adm_number(self):
        adm_number = self.cleaned_data.get('admission_number')
        if Student.objects.filter(adm_number=adm_number).exists():
            raise forms.ValidationError("A student with this admission number already exists.")
        return adm_number
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Student.objects.filter(email=email).exists():
            raise forms.ValidationError("A student with this email already exists.")
        return email

class StudentLoginForm(forms.Form):
    """
    Form for student login using admission number
    """
    adm_number = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)